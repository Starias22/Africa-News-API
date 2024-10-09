from pyspark.sql import SparkSession
from pyspark.sql.functions import lower, udf, when, col
from pyspark.sql.types import StringType
import unidecode
from datetime import datetime
from pyspark.sql import functions as F

# Initialize Spark session
spark = SparkSession.builder.appName("LoadCSV").getOrCreate()

# Load all CSV files in the directory (use wildcard to match file names)

df = spark.read \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("multiLine", True) \
    .csv("/home/starias/africa_news_api/staging_area/raw_news/2024-10-08/18/*.csv", header=True, inferSchema=True)

df = df.dropDuplicates()

df = df.withColumn("country", lower(df["country"])).withColumn("category", lower(df["category"]))

# Step 3: Define UDF to remove accents
def remove_accents(text):
    if text:
        return unidecode.unidecode(text)
    return None

# Step 4: Register the UDF
remove_accents_udf = udf(remove_accents, StringType())

# Step 5: Apply the UDF to the 'countries' column
df = df.withColumn("country", remove_accents_udf(df["country"])).withColumn("category", remove_accents_udf(df["category"]))


country_translation = {
    "afrique du sud": "south africa",
    "algerie": "algeria",
    "cameroun": "cameroon",
    "cap-vert": "cabo verde",
    "centrafrique": "central african republic",
    "comores": "comoros",
    "congo-brazzaville": "republic of the congo",
    "congo-kinshasa": "democratic republic of the congo",
    "cote d'ivoire": "ivory coast",
    "egypte": "egypt",
    "erythree": "eritrea",
    "ethiopie": "ethiopia",
    "gambie": "gambia",
    "guinee": "guinea",
    "guinee-bissau": "guinea-bissau",
    "guinea bissau": "guinea-bissau",
    "guinee equatoriale": "equatorial guinea",
    "kenya": "kenya",
    "libye": "libya",
    "maroc": "morocco",
    "maurice": "mauritius",
    "mauritanie": "mauritania",
    "mozambique": "mozambique",
    "namibie": "namibia",
    "niger": "niger",
    "nigeria": "nigeria",
    "ouganda": "uganda",
    "rd congo": "democratic republic of the congo",
    "republique du congo": "republic of the congo",
    "sao tome-et-principe": "sao tome & principe",
    "senegal": "senegal",
    "seychelles": "seychelles",
    "somalie": "somalia",
    "soudan": "sudan",
    "soudan du sud": "south sudan",
    "tanzanie": "tanzania",
    "tchad": "chad",
    "tunisie": "tunisia",
    "zambie": "zambia",
    "zimbabwe": "zimbabwe",
    "afrique":"africa"
}


# UDF to map French country names to their English equivalents
def translate_country(country):
    return country_translation.get(country, country)  # Default to original if no match found

translate_country_udf = udf(translate_country, StringType())

df = df.withColumn("country", translate_country_udf(df["country"]))

df = df.withColumn(
    "country", 
    when(col("country").isin("africa", "monde", "moyen-orient"), None)
    .otherwise(col("country"))
)

# Show the transformed DataFrame
df.show(truncate=False)



# Show the loaded data
df.filter((df["source"] == "") | (df["source"].isNull())).show(3000)

countries_df = df.select("country").distinct().orderBy("country")


countries_df.show(10000, truncate=False)
# Apply the grouping
df = df.withColumn(
    "category",
    F.when(col("category").contains("sport") | col("category").contains("athletisme"), "sport")
   .when(col("category").isin("economie"), "business-economy-finance")
    .when(col("category").isin("politique"), "politics")
    .when(col("category").isin("technologie"), "technology")
    .when(col("category").isin("sante"), "health-wellness")
    .when(col("category").isin("societe"), "society")
    .when(col("category").isin("securite"), "security")
    .when(col("category").isin("beaute - mode"), "lifestyle")
    .when(col("category").isin("celebrite"), "celebrity")
    .when(col("category").isin("non classifie(e)", "actus"), None)
    .when(col("category").isin("ecoles - formations","education"), "education")
    .when(col("category").isin("diplomatie"), "diplomacy")
    .when(col("category").isin( "analyse et decryptage"), "analysis-interpretation")
    .when(col("category").isin( "faits divers"), "miscellaneous")
    .otherwise(col("category"))
)

categories_df = df.select("category").distinct().orderBy("category")
categories_df.show(10000, truncate=False)

# Split the publication_date into day, month, and year
df = df.withColumn("day", 
                   F.when(F.col("publication_date").isNotNull(), 
                          F.split(F.col("publication_date"), " ")[0])
                   .otherwise(None))

df = df.withColumn("month", 
                   F.when(F.col("publication_date").isNotNull(), 
                          F.split(F.col("publication_date"), " ")[1])
                   .otherwise(None))

df = df.withColumn("year", 
                   F.when(F.col("publication_date").isNotNull(), 
                          F.split(F.col("publication_date"), " ")[2])
                   .otherwise(None))

df = df.withColumn("day", 
                   F.regexp_replace(F.col("day"), "(nd|st|th|rd)$", ""))

df = df.withColumn(
    "month",
    F.when(col("month").contains("janv"), 1)
     .when(col("month").contains("févr"), 2)
     .when(col("month").contains("mars"), 3)
     .when(col("month").contains("avr"), 4)
     .when(col("month").contains("mai"), 5)
     .when(col("month").contains("juin"), 6)
     .when(col("month").contains("juil"), 7)
     .when(col("month").isin("août", "aout"), 8)
     .when(col("month").contains("sept"),9)
     .when(col("month").contains("oct"), 10)
     .when(col("month").contains("nov"), 11)
     .when(col("month").contains("dec"), 12)
     .otherwise(None)
)

# Construct the publication_date and convert it to an integer Unix timestamp
df = df.withColumn("publication_date", 
                   F.when(col("month").isNotNull(), 
                          F.unix_timestamp(F.concat_ws(" ", 
                                                      F.lpad(F.col("day").cast("string"), 2, '0'), 
                                                      F.lit("01"),  # Placeholder for day of month
                                                      F.col("year")), 
                                         "dd MM yyyy"))
                   .otherwise(None))  # Keep the original value if month is NULL


# Convert Unix timestamp back to date format 'yyyy-MM-dd'
df = df.withColumn("publication_date", F.from_unixtime(F.col("publication_date"), "yyyy-MM-dd"))

df.select(["publication_date", "day", "month", "year"]).show()

# Remove the day, month, and year columns
df = df.drop("day", "month", "year")



 # Get the current datetime
now = datetime.now()

# Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
formatted_date = now.strftime('%Y-%m-%d')
formatted_hour = now.strftime('%H')  # This will be '02' if the hour is 2

        
filepath = f'/home/starias/africa_news_api/staging_area/transformed_news/{formatted_date}/{formatted_hour}'


# Save the DataFrame to a CSV file with proper quoting
df.write.option("quote", '"').option("escape", '"').csv(filepath, header=True, mode='overwrite')

spark.stop()