PGDMP  /    +                 |            api_agriculture    16.0    16.0 )    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16484    api_agriculture    DATABASE     �   CREATE DATABASE api_agriculture WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE api_agriculture;
                super_admin_agriculture    false            �            1259    16533    chimical_element    TABLE     �   CREATE TABLE public.chimical_element (
    element_code character varying(5) NOT NULL,
    unit character varying(20) NOT NULL,
    wording_element character varying(20)
);
 $   DROP TABLE public.chimical_element;
       public         heap    postgres    false            �            1259    16494    culture    TABLE     �   CREATE TABLE public.culture (
    id_culture smallint NOT NULL,
    plot_number smallint NOT NULL,
    production_code smallint NOT NULL,
    start_date date,
    end_date date,
    quantity_harvested numeric NOT NULL
);
    DROP TABLE public.culture;
       public         heap    postgres    false            �            1259    16518    date    TABLE     5   CREATE TABLE public.date (
    date date NOT NULL
);
    DROP TABLE public.date;
       public         heap    postgres    false            �            1259    16523 
   fertilizer    TABLE     �   CREATE TABLE public.fertilizer (
    id_fertilizer smallint NOT NULL,
    unit character varying(20) NOT NULL,
    fertilizer_name character varying(20)
);
    DROP TABLE public.fertilizer;
       public         heap    postgres    false            �            1259    16487    plot    TABLE     �   CREATE TABLE public.plot (
    plot_number smallint NOT NULL,
    surface numeric,
    plot_name character varying(20),
    coordinates character varying(20)
);
    DROP TABLE public.plot;
       public         heap    postgres    false            �            1259    16528    possess    TABLE     �   CREATE TABLE public.possess (
    id_fertilizer smallint NOT NULL,
    element_code character varying(5) NOT NULL,
    value character varying(255)
);
    DROP TABLE public.possess;
       public         heap    postgres    false            �            1259    16501 
   production    TABLE     �   CREATE TABLE public.production (
    production_code smallint NOT NULL,
    unit character varying(20) NOT NULL,
    production_name character varying(20)
);
    DROP TABLE public.production;
       public         heap    postgres    false            �            1259    16511    spread    TABLE     �   CREATE TABLE public.spread (
    id_fertilizer smallint NOT NULL,
    plot_number smallint NOT NULL,
    date date NOT NULL,
    quantity_spread numeric NOT NULL
);
    DROP TABLE public.spread;
       public         heap    postgres    false            �            1259    16506    unit    TABLE     F   CREATE TABLE public.unit (
    unit character varying(20) NOT NULL
);
    DROP TABLE public.unit;
       public         heap    postgres    false            �          0    16533    chimical_element 
   TABLE DATA           O   COPY public.chimical_element (element_code, unit, wording_element) FROM stdin;
    public          postgres    false    223   30       �          0    16494    culture 
   TABLE DATA           u   COPY public.culture (id_culture, plot_number, production_code, start_date, end_date, quantity_harvested) FROM stdin;
    public          postgres    false    216   o0       �          0    16518    date 
   TABLE DATA           $   COPY public.date (date) FROM stdin;
    public          postgres    false    220   �0       �          0    16523 
   fertilizer 
   TABLE DATA           J   COPY public.fertilizer (id_fertilizer, unit, fertilizer_name) FROM stdin;
    public          postgres    false    221   �0       �          0    16487    plot 
   TABLE DATA           L   COPY public.plot (plot_number, surface, plot_name, coordinates) FROM stdin;
    public          postgres    false    215   �0       �          0    16528    possess 
   TABLE DATA           E   COPY public.possess (id_fertilizer, element_code, value) FROM stdin;
    public          postgres    false    222   c1       �          0    16501 
   production 
   TABLE DATA           L   COPY public.production (production_code, unit, production_name) FROM stdin;
    public          postgres    false    217   �1       �          0    16511    spread 
   TABLE DATA           S   COPY public.spread (id_fertilizer, plot_number, date, quantity_spread) FROM stdin;
    public          postgres    false    219   �1       �          0    16506    unit 
   TABLE DATA           $   COPY public.unit (unit) FROM stdin;
    public          postgres    false    218   �1       J           2606    16537 &   chimical_element chimical_element_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.chimical_element
    ADD CONSTRAINT chimical_element_pkey PRIMARY KEY (element_code);
 P   ALTER TABLE ONLY public.chimical_element DROP CONSTRAINT chimical_element_pkey;
       public            postgres    false    223            <           2606    16500    culture culture_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.culture
    ADD CONSTRAINT culture_pkey PRIMARY KEY (id_culture);
 >   ALTER TABLE ONLY public.culture DROP CONSTRAINT culture_pkey;
       public            postgres    false    216            D           2606    16522    date date_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.date
    ADD CONSTRAINT date_pkey PRIMARY KEY (date);
 8   ALTER TABLE ONLY public.date DROP CONSTRAINT date_pkey;
       public            postgres    false    220            F           2606    16527    fertilizer fertilizer_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.fertilizer
    ADD CONSTRAINT fertilizer_pkey PRIMARY KEY (id_fertilizer);
 D   ALTER TABLE ONLY public.fertilizer DROP CONSTRAINT fertilizer_pkey;
       public            postgres    false    221            :           2606    16493    plot plot_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.plot
    ADD CONSTRAINT plot_pkey PRIMARY KEY (plot_number);
 8   ALTER TABLE ONLY public.plot DROP CONSTRAINT plot_pkey;
       public            postgres    false    215            H           2606    16532    possess possess_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.possess
    ADD CONSTRAINT possess_pkey PRIMARY KEY (id_fertilizer, element_code);
 >   ALTER TABLE ONLY public.possess DROP CONSTRAINT possess_pkey;
       public            postgres    false    222    222            >           2606    16505    production production_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.production
    ADD CONSTRAINT production_pkey PRIMARY KEY (production_code);
 D   ALTER TABLE ONLY public.production DROP CONSTRAINT production_pkey;
       public            postgres    false    217            B           2606    16517    spread spread_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.spread
    ADD CONSTRAINT spread_pkey PRIMARY KEY (id_fertilizer, plot_number, date);
 <   ALTER TABLE ONLY public.spread DROP CONSTRAINT spread_pkey;
       public            postgres    false    219    219    219            @           2606    16510    unit unit_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.unit
    ADD CONSTRAINT unit_pkey PRIMARY KEY (unit);
 8   ALTER TABLE ONLY public.unit DROP CONSTRAINT unit_pkey;
       public            postgres    false    218            T           2606    16583 &   chimical_element chimical_element_unit    FK CONSTRAINT     �   ALTER TABLE ONLY public.chimical_element
    ADD CONSTRAINT chimical_element_unit FOREIGN KEY (unit) REFERENCES public.unit(unit) NOT VALID;
 P   ALTER TABLE ONLY public.chimical_element DROP CONSTRAINT chimical_element_unit;
       public          postgres    false    218    4672    223            K           2606    16538    culture culture_plot_number    FK CONSTRAINT     �   ALTER TABLE ONLY public.culture
    ADD CONSTRAINT culture_plot_number FOREIGN KEY (plot_number) REFERENCES public.plot(plot_number) NOT VALID;
 E   ALTER TABLE ONLY public.culture DROP CONSTRAINT culture_plot_number;
       public          postgres    false    4666    215    216            L           2606    16543    culture culture_production_code    FK CONSTRAINT     �   ALTER TABLE ONLY public.culture
    ADD CONSTRAINT culture_production_code FOREIGN KEY (production_code) REFERENCES public.production(production_code) NOT VALID;
 I   ALTER TABLE ONLY public.culture DROP CONSTRAINT culture_production_code;
       public          postgres    false    216    217    4670            Q           2606    16568    fertilizer fertilizer_unit    FK CONSTRAINT     �   ALTER TABLE ONLY public.fertilizer
    ADD CONSTRAINT fertilizer_unit FOREIGN KEY (unit) REFERENCES public.unit(unit) NOT VALID;
 D   ALTER TABLE ONLY public.fertilizer DROP CONSTRAINT fertilizer_unit;
       public          postgres    false    4672    221    218            R           2606    16578    possess posess_element_code    FK CONSTRAINT     �   ALTER TABLE ONLY public.possess
    ADD CONSTRAINT posess_element_code FOREIGN KEY (element_code) REFERENCES public.chimical_element(element_code) NOT VALID;
 E   ALTER TABLE ONLY public.possess DROP CONSTRAINT posess_element_code;
       public          postgres    false    222    223    4682            S           2606    16573    possess possess_id_fertilizer    FK CONSTRAINT     �   ALTER TABLE ONLY public.possess
    ADD CONSTRAINT possess_id_fertilizer FOREIGN KEY (id_fertilizer) REFERENCES public.fertilizer(id_fertilizer) NOT VALID;
 G   ALTER TABLE ONLY public.possess DROP CONSTRAINT possess_id_fertilizer;
       public          postgres    false    222    221    4678            M           2606    16548    production production_unit    FK CONSTRAINT     �   ALTER TABLE ONLY public.production
    ADD CONSTRAINT production_unit FOREIGN KEY (unit) REFERENCES public.unit(unit) NOT VALID;
 D   ALTER TABLE ONLY public.production DROP CONSTRAINT production_unit;
       public          postgres    false    217    4672    218            N           2606    16563    spread spread_date    FK CONSTRAINT     y   ALTER TABLE ONLY public.spread
    ADD CONSTRAINT spread_date FOREIGN KEY (date) REFERENCES public.date(date) NOT VALID;
 <   ALTER TABLE ONLY public.spread DROP CONSTRAINT spread_date;
       public          postgres    false    4676    219    220            O           2606    16558    spread spread_id_fertilizer    FK CONSTRAINT     �   ALTER TABLE ONLY public.spread
    ADD CONSTRAINT spread_id_fertilizer FOREIGN KEY (id_fertilizer) REFERENCES public.fertilizer(id_fertilizer) NOT VALID;
 E   ALTER TABLE ONLY public.spread DROP CONSTRAINT spread_id_fertilizer;
       public          postgres    false    4678    221    219            P           2606    16553    spread spread_plot_number    FK CONSTRAINT     �   ALTER TABLE ONLY public.spread
    ADD CONSTRAINT spread_plot_number FOREIGN KEY (plot_number) REFERENCES public.plot(plot_number) NOT VALID;
 C   ALTER TABLE ONLY public.spread DROP CONSTRAINT spread_plot_number;
       public          postgres    false    219    4666    215            �   ,   x�34261��N�L�I"#.C��)g:gFvNNvVf>W� �]
      �   .   x�36�4 B#C]c]#K�? �� ]�i�e�G�9F��� ���      �      x�3202�54�50����� ��      �      x�3��N��K�M�2��2b���� N�      �   T   x�3�423�LKMK�LO�JO�2�42�L�I"ά����Ԣ|.tUƜ&��~��
)�
9�%����E)�y�%��\�c���� ONP      �      x�3�44261�L�=... "Fy      �      x�3��N��K�M�2��b���� V�(      �      x������ � �      �      x��N�J����� ��     