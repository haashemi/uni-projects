create type user_role as enum ('user', 'admin');

create table users (
    id              uuid        primary key default gen_random_uuid(),
    name            text        not null,
    phone           varchar(10) not null unique check (phone ~ '^9'),
    national_code   varchar(10) not null unique check (national_code ~ '^[0-9]+$'),
    role            user_role   not null default 'user'
);

create table ads (
    id          uuid        primary key default gen_random_uuid(),
    user_id     uuid        not null    references users(id) on delete cascade,
    name        text        not null,
    audiences   text[]      not null,
    image_url   text        not null,
    target_url  text        not null,
    since_date  date        not null,
    until_date  date        not null,
    created_at  timestamptz not null default now(),

    constraint chk_ads_valid_dates check (since_date <= until_date)
);

create table ad_clicks (
    id          bigint  primary key generated always as identity,
    ad_id       uuid    not null    references ads(id) on delete cascade,
    hash        text    not null    unique,
    asn         text,
    asn_name    text,
    asn_country text,
    platform    text    not null,
    browser     text
);

create table payments (
    id              uuid    primary key default gen_random_uuid(),
    ad_id           uuid    not null    references ads(id) on delete restrict,
    user_id         uuid    not null    references users(id) on delete restrict,
    status          text    not null,
    gateway         text    not null,
    amount          int     not null,
    transaction_id  text    not null    unique,
    gateway_data    jsonb
);
