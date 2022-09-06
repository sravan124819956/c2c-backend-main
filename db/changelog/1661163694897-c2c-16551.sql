--liquibase formatted sql

--changeset jufishan:1661163694897

CREATE SCHEMA IF NOT EXISTS medupdates;

CREATE TYPE medupdates.journal_access_enum AS ENUM (
    'Public',
    'Private'
);

CREATE TYPE medupdates.journal_type_enum AS ENUM (
    'Premium',
    'Paid'
);

CREATE TYPE medupdates.action_by_user_type_enum AS ENUM (
    '1',
    '2',
    '3',
    '4'
);

CREATE TYPE medupdates.reaction_enum AS ENUM (
     'Undecided',
     'Like',
     'Hate'
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.specialties
(
    id uuid DEFAULT uuid_generate_v4(),
    name character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id)
);

CREATE TABLE medupdates.journals
(
    id uuid DEFAULT uuid_generate_v4(),
    specialty_id uuid NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL,
    status integer DEFAULT 0,
    featured_for_day boolean DEFAULT false,
    featured_for_user boolean DEFAULT false,
    ext_weblink character varying,
    ext_name character varying,
    ext_type medupdates.journal_type_enum,
    ext_access medupdates.journal_access_enum,
    scheduled_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (specialty_id)
        REFERENCES public.specialties (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE medupdates.journal_documents
(
    id uuid DEFAULT uuid_generate_v4(),
    journal_id uuid NOT NULL,
    title character varying,
    path character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (journal_id)
        REFERENCES medupdates.journals (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE medupdates.journal_reactions
(
    id uuid,
    journal_id uuid NOT NULL,
    user_id uuid,
    reaction medupdates.reaction_enum,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (journal_id)
        REFERENCES medupdates.journals (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE medupdates.journal_user_actions
(
    id uuid DEFAULT uuid_generate_v4(),
    journal_id uuid NOT NULL,
    action_name integer NOT NULL,
    action_by_userid uuid NOT NULL,
    action_by_usertype medupdates.action_by_user_type_enum NOT NULL,
    action_at timestamp without time zone NOT NULL,
    user_agent character varying(255),
    PRIMARY KEY (id),
    FOREIGN KEY (journal_id)
        REFERENCES medupdates.journals (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
