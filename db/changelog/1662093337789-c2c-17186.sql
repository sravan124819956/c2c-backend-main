--liquibase formatted sql

--changeset jufishan:1662093337789

ALTER TABLE IF EXISTS medupdates.journals
    ADD COLUMN IF NOT EXISTS deleted_at timestamp without time zone;
