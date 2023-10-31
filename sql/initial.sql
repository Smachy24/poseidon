/*
Create a group
*/
CREATE ROLE super_admin_agriculture 
WITH NOLOGIN;

/*
Create database
*/
CREATE DATABASE api_agriculture;

/*
Transfer ownership to group
*/
ALTER DATABASE api_agriculture 
OWNER TO super_admin_agriculture;

/*
Grant permissions to group
*/
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES
IN SCHEMA public
TO super_admin_agriculture;

/*
Give CREATE permissions to backend group
*/
GRANT CREATE 
ON SCHEMA public
TO super_admin_agriculture;

/*
Create new users
*/
CREATE ROLE agriculteur
WITH LOGIN
PASSWORD 'password'
INHERIT;

/*
Assign backend group permissions to users
*/
GRANT super_admin_agriculture 
TO agriculteur;

