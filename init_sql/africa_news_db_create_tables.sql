-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: africa_news_db | type: DATABASE --
-- DROP DATABASE IF EXISTS africa_news_db;
-- CREATE DATABASE africa_news_db;
-- ddl-end --


-- object: public.author | type: TABLE --
-- DROP TABLE IF EXISTS public.author CASCADE;
CREATE TABLE public.author (
	author_id serial NOT NULL,
	author_name varchar(100),
	author_url text,
	CONSTRAINT author_pk PRIMARY KEY (author_id)
);
-- ddl-end --
ALTER TABLE public.author OWNER TO postgres;
-- ddl-end --

-- object: public.country | type: TABLE --
-- DROP TABLE IF EXISTS public.country CASCADE;
CREATE TABLE public.country (
	country_id smallserial NOT NULL,
	country_name varchar(100),
	country_code char(2) NOT NULL,
	CONSTRAINT country_pk PRIMARY KEY (country_id)
);
-- ddl-end --
ALTER TABLE public.country OWNER TO postgres;
-- ddl-end --

-- object: public.language | type: TABLE --
-- DROP TABLE IF EXISTS public.language CASCADE;
CREATE TABLE public.language (
	lang_id smallserial NOT NULL,
	lang_name varchar(100) NOT NULL,
	lang_code char(2) NOT NULL,
	CONSTRAINT language_pk PRIMARY KEY (lang_id)
);
-- ddl-end --
ALTER TABLE public.language OWNER TO postgres;
-- ddl-end --

-- object: public.category | type: TABLE --
-- DROP TABLE IF EXISTS public.category CASCADE;
CREATE TABLE public.category (
	category_id smallserial NOT NULL,
	category_name varchar(100),
	CONSTRAINT category_pk PRIMARY KEY (category_id)
);
-- ddl-end --
ALTER TABLE public.category OWNER TO postgres;
-- ddl-end --

-- object: public.extractor | type: TABLE --
-- DROP TABLE IF EXISTS public.extractor CASCADE;
CREATE TABLE public.extractor (
	extractor_id smallserial NOT NULL,
	extractor_name varchar(100) NOT NULL,
	extractor_description text,
	extractor_url text,
	CONSTRAINT extractor_pk PRIMARY KEY (extractor_id)
);
-- ddl-end --
ALTER TABLE public.extractor OWNER TO postgres;
-- ddl-end --

-- object: public.article | type: TABLE --
-- DROP TABLE IF EXISTS public.article CASCADE;
CREATE TABLE public.article (
	article_id serial NOT NULL,
	author_id integer NOT NULL,
	category_id smallint NOT NULL,
	extractor_id smallint NOT NULL,
	country_id smallint NOT NULL,
	lang_id smallint NOT NULL,
	publication_date date,
	title text,
	description text,
	img_url text,
	url text,
	content_preview text,
	content text,
	source varchar(100),
	author_id_author integer,
	lang_id_language smallint,
	extractor_id_extractor smallint,
	country_id_country smallint,
	category_id_category smallint,
	CONSTRAINT article_pk PRIMARY KEY (article_id)
);
-- ddl-end --
ALTER TABLE public.article OWNER TO postgres;
-- ddl-end --

-- object: author_fk | type: CONSTRAINT --
-- ALTER TABLE public.article DROP CONSTRAINT IF EXISTS author_fk CASCADE;
ALTER TABLE public.article ADD CONSTRAINT author_fk FOREIGN KEY (author_id_author)
REFERENCES public.author (author_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: language_fk | type: CONSTRAINT --
-- ALTER TABLE public.article DROP CONSTRAINT IF EXISTS language_fk CASCADE;
ALTER TABLE public.article ADD CONSTRAINT language_fk FOREIGN KEY (lang_id_language)
REFERENCES public.language (lang_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: extractor_fk | type: CONSTRAINT --
-- ALTER TABLE public.article DROP CONSTRAINT IF EXISTS extractor_fk CASCADE;
ALTER TABLE public.article ADD CONSTRAINT extractor_fk FOREIGN KEY (extractor_id_extractor)
REFERENCES public.extractor (extractor_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: country_fk | type: CONSTRAINT --
-- ALTER TABLE public.article DROP CONSTRAINT IF EXISTS country_fk CASCADE;
ALTER TABLE public.article ADD CONSTRAINT country_fk FOREIGN KEY (country_id_country)
REFERENCES public.country (country_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: category_fk | type: CONSTRAINT --
-- ALTER TABLE public.article DROP CONSTRAINT IF EXISTS category_fk CASCADE;
ALTER TABLE public.article ADD CONSTRAINT category_fk FOREIGN KEY (category_id_category)
REFERENCES public.category (category_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: africa_news_db_create_tables | type: Generic SQL Object --
-- dd
-- ddl-end --


