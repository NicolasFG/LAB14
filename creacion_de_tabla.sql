CREATE TABLE covid_vaccination_vs_mortality (
    id integer,
    country varchar(100),
    iso_code varchar(100),
    date date,
    total_vaccinations float,
    people_vaccinated float,
    people_fully_vaccinated float,
    new_deaths float,
    population float,
    ratio float
)