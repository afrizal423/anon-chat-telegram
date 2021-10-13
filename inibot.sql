--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0 (Debian 14.0-1.pgdg110+1)
-- Dumped by pg_dump version 14.0 (Debian 14.0-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: tbl_iddle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_iddle (
    iddle_uuid character varying(255) NOT NULL,
    id_user character varying(255) NOT NULL,
    status boolean,
    updated_at timestamp with time zone DEFAULT now(),
    mssg_id character varying(100)
);


ALTER TABLE public.tbl_iddle OWNER TO postgres;

--
-- Name: tbl_partner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_partner (
    partner_uuid character varying(255) NOT NULL,
    id_user_pertama character varying(255) NOT NULL,
    id_user_kedua character varying(255),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.tbl_partner OWNER TO postgres;

--
-- Name: tbl_pengguna; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_pengguna (
    user_uuid character varying(255) NOT NULL,
    id_user character varying(255) NOT NULL,
    username_user character varying(255),
    firstname_user character varying(255),
    lastname_user character varying(255),
    jeniskelamin_user character varying(2),
    ketertarikan_user character varying(2),
    umur_user integer,
    joined_at timestamp without time zone
);


ALTER TABLE public.tbl_pengguna OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
cf92a61b6cdf
\.


--
-- Data for Name: tbl_iddle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_iddle (iddle_uuid, id_user, status, updated_at, mssg_id) FROM stdin;
b13ccf38-2318-4c78-adff-1a43a51fa065	576507972	f	2021-10-12 08:45:22.876108+00	\N
df8fbd40-d6e8-490f-b302-e6da9647dacc	784718429	f	2021-10-12 12:54:24.829168+00	\N
d8e5536b-9bd0-46ad-acba-d468fd94d2e4	2033673942	f	2021-10-12 09:15:47.822714+00	\N
ac7bb7b4-157a-42c3-a581-68db29594554	551877623	f	2021-10-12 09:47:36.664494+00	\N
\.


--
-- Data for Name: tbl_partner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_partner (partner_uuid, id_user_pertama, id_user_kedua, updated_at) FROM stdin;
\.


--
-- Data for Name: tbl_pengguna; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl_pengguna (user_uuid, id_user, username_user, firstname_user, lastname_user, jeniskelamin_user, ketertarikan_user, umur_user, joined_at) FROM stdin;
96bc2ffa-bd3c-44e9-b2a2-9a950f4f0721	2033673942	ijaldev	IjaL	Dev	P	L	19	2021-12-10 16:15:47
7bb3f864-31f5-4fd8-b144-532d8805675a	551877623	\N	Ifwatul	Nurul	P	L	21	2021-12-10 16:47:36
bcddb68e-ae9b-4844-879d-b7eabaa6e718	784718429	\N	Nadia	\N	P	L	22	2021-12-10 19:54:24
d1f0e2d5-3fb0-4e8e-bf42-107eb893e17f	576507972	af_rizal	Afrizal	M	L	P	22	2021-12-10 15:45:22
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: tbl_iddle tbl_iddle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_iddle
    ADD CONSTRAINT tbl_iddle_pkey PRIMARY KEY (iddle_uuid);


--
-- Name: tbl_partner tbl_partner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_partner
    ADD CONSTRAINT tbl_partner_pkey PRIMARY KEY (partner_uuid);


--
-- Name: tbl_pengguna tbl_pengguna_id_user_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_pengguna
    ADD CONSTRAINT tbl_pengguna_id_user_key UNIQUE (id_user);


--
-- Name: tbl_pengguna tbl_pengguna_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_pengguna
    ADD CONSTRAINT tbl_pengguna_pkey PRIMARY KEY (user_uuid);


--
-- Name: tbl_iddle tbl_iddle_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_iddle
    ADD CONSTRAINT tbl_iddle_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.tbl_pengguna(id_user);


--
-- Name: tbl_partner tbl_partner_id_user_kedua_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_partner
    ADD CONSTRAINT tbl_partner_id_user_kedua_fkey FOREIGN KEY (id_user_kedua) REFERENCES public.tbl_pengguna(id_user);


--
-- Name: tbl_partner tbl_partner_id_user_pertama_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_partner
    ADD CONSTRAINT tbl_partner_id_user_pertama_fkey FOREIGN KEY (id_user_pertama) REFERENCES public.tbl_pengguna(id_user);


--
-- PostgreSQL database dump complete
--

