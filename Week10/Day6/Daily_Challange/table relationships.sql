CREATE TABLE IF NOT EXISTS public.book
(
    book_id integer NOT NULL DEFAULT nextval('book_book_id_seq'::regclass),
    title character varying(50) COLLATE pg_catalog."default" NOT NULL,
    author character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT book_pkey PRIMARY KEY (book_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.book
    OWNER to postgres;

CREATE TABLE public.customer_profile
(
    id integer NOT NULL DEFAULT nextval('customer_profile_id_seq'::regclass),
    "isLoggedIn" boolean DEFAULT false,
    customer_id integer,
    CONSTRAINT customer_profile_pkey PRIMARY KEY (id),
    CONSTRAINT customer_profile_customer_id_key UNIQUE (customer_id),
    CONSTRAINT customer_profile_customer_id_fkey FOREIGN KEY (customer_id)
        REFERENCES public.customer (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customer_profile
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.customers
(
    id integer,
    first_name character varying(100) COLLATE pg_catalog."default",
    last_name character varying(100) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.firsttab
(
    id integer,
    name character varying(10) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.firsttab
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.items
(
    id integer,
    item_name character varying(100) COLLATE pg_catalog."default",
    price integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.items
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.library
(
    book_fk_id integer NOT NULL,
    student_fk_id integer NOT NULL,
    borrowed_date date,
    CONSTRAINT library_pkey PRIMARY KEY (book_fk_id, student_fk_id),
    CONSTRAINT library_book_fk_id_fkey FOREIGN KEY (book_fk_id)
        REFERENCES public.book (book_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT library_student_fk_id_fkey FOREIGN KEY (student_fk_id)
        REFERENCES public.student (student_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.library
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.student
(
    student_id integer NOT NULL DEFAULT nextval('student_student_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    age integer,
    CONSTRAINT student_pkey PRIMARY KEY (student_id),
    CONSTRAINT student_name_key UNIQUE (name),
    CONSTRAINT student_age_check CHECK (age <= 15)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.student
    OWNER to postgres;
