/*
Create a group
*/
CREATE ROLE super_admin 
WITH NOLOGIN;

/*
Create database
*/
CREATE DATABASE poseidon;

/*
Transfer ownership to group
*/
ALTER DATABASE poseidon 
OWNER TO super_admin;

/*
Grant permissions to group
*/
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES
IN SCHEMA public
TO super_admin;

/*
Give CREATE permissions to backend group
*/
GRANT CREATE 
ON SCHEMA public
TO super_admin;

/*
Create new users
*/
CREATE ROLE username
WITH LOGIN
PASSWORD 'password'
INHERIT;

/*
Assign backend group permissions to users
*/
GRANT super_admin 
TO username;

