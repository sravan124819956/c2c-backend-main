--liquibase formatted sql

--changeset jufishan:1661428618745

ALTER TABLE IF EXISTS medupdates.journals
    ALTER COLUMN specialty_id DROP NOT NULL;