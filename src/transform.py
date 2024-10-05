from pyspark.sql import SparkSession
from pyspark.sql.functions import lower, udf, when, col
from pyspark.sql.types import StringType
import unidecode

# Initialize Spark session
spark = SparkSession.builder.appName("LoadCSV").getOrCreate()

# Load all CSV files in the directory (use wildcard to match file names)

df = spark.read \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("multiLine", True) \
    .csv("/home/starias/africa_news_api/staging_area/raw_news/2024-10-05/16/*.csv", header=True, inferSchema=True)

df = df.dropDuplicates()

df = df.withColumn("countries", lower(df["countries"])).withColumn("category", lower(df["category"]))

# Step 3: Define UDF to remove accents
def remove_accents(text):
    if text:
        return unidecode.unidecode(text)
    return None

# Step 4: Register the UDF
remove_accents_udf = udf(remove_accents, StringType())

# Step 5: Apply the UDF to the 'countries' column
df = df.withColumn("countries", remove_accents_udf(df["countries"])).withColumn("category", remove_accents_udf(df["category"]))


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

#"moyen-orient" from the list as well, alongside "africa" and "monde".

# UDF to map French country names to their English equivalents
def translate_country(country):
    return country_translation.get(country, country)  # Default to original if no match found

translate_country_udf = udf(translate_country, StringType())

df = df.withColumn("countries", translate_country_udf(df["countries"]))

df = df.withColumn(
    "countries", 
    when(col("countries").isin("africa", "monde", "moyen-orient"), None)
    .otherwise(col("countries"))
)


category_translation = {
    "actus": "news",
    "afrique - sport": "africa - sport",
    "analyse et decryptage": "analysis and decryption",
    "athletisme": "athletics",
    "beaute - mode": "beauty - fashion",
    "benin - sport": "benin - sport",
    "celebrite": "celebrity",
    "contribution": "contribution",
    "diplomatie": "diplomacy",
    "ecoles - formations": "schools - training",
    "economie": "economy",
    "education": "education",
    "faits divers": "various facts",
    "football": "football",
    "monde - sport": "world - sport",
    "non classifie(e)": "uncategorized",
    "politique": "politics",
    "sante": "health",
    "securite": "security",
    "showbiz": "showbiz",
    "societe": "society",
    "technologie": "technology",
}



# Show the transformed DataFrame
df.show(truncate=False)



# Show the loaded data
df.filter((df["source"] == "") | (df["source"].isNull())).show(3000)


m=df.count()
print(m)

countries_df = df.select("countries").distinct().orderBy("countries")


n=countries_df.count()

print(n)
print("****************")
countries_df.show(10000, truncate=False)

categories_df = df.select("category").distinct().orderBy("category")
##categories_df.show(10000, truncate=False)



spark.stop()