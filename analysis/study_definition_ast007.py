
# Import functions
import json
from ssl import ALERT_DESCRIPTION_DECODE_ERROR
from xmlrpc.server import resolve_dotted_attribute
import pandas as pd

from cohortextractor import (
    StudyDefinition, 
    patients, 
    codelist, 
    Measure
)

# Import codelists
from codelists import *

from config import start_date, end_date, codelist_path, demographics

codelist_df = pd.read_csv(codelist_path)
codelist_expectation_codes = codelist_df['code'].unique()


# Specify study definition

study = StudyDefinition(
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.satisfying(
        """
        # Define general population parameters
        (NOT died) AND
        # Define GMS registration status
        gms_reg_status AND
        # Asthma list size age restriction
        age >= 6
        """,
    ),
    # Include asthma variables
    **ast_reg_variables,
    # Include demographic variables
    **demographic_variables,
)

##############################
# Rule 1 

# Asthma review occurring within the last 12 months
    ast_rev=patients.with_these_clinical_events(
            codelist = rev_writ_codes, #THIS DOESN'T WORK - USE PATIENTS.SATISFYING
            between=["first_day_of_month(index_date) - 11 months","last_day_of_month(index_date)"],
            returning="binary_flag",
            include_date_of_match=True,
            date_format="YYYY-MM-DD",
            find_last_match_in_period=True,
            return_expectations = {
                "date": {"earliest": "2019-03-01", "latest": "index_date"},
                "incidence": 0.9
            },
        ),     

# Asthma written personalised asthma plan  on the same day and within the last 12 months
    ast_writpastp=patients.with_these_clinical_events(
            codelist = writpastp_cod, #THIS DOESN'T WORK - USE PATIENTS.SATISFYING
            between=["ast_rev_date - 1 day","ast_rev_date"],
            returning="date",
            date_format="YYYY-MM-DD",
            find_last_match_in_period=True,
            return_expectations = {
                "date": {"earliest": "2019-03-01", "latest": "index_date"},
                "incidence": 0.9
            },
        ),         

# Asthma control assessment within 1 month of asthma review date
    astcontass_dat=patients.with_these_clinical_events(
            codelist = astcontass_cod,
            between=["ast_rev_date -  1 month", "ast_rev_date"],
            returning="binary_flag",
            return_expectations={"incidence": 0.10},
        ),

# Asthma exacerbations recorded within 1 month of asthma review date
    astexac_dat=patients.with_these_clinical_events(
            codelist = astexacb_cod,
            between=["ast_rev_date - 1 month", "ast_rev_date"],
            returning="binary_flag",
            return_expectations={"incidence": 0.10},
        ),

# Rule 1 logic
    ast007_rule1=patients.satisfying(
            """
            ast_rev AND
            astcontass_dat AND
            astexac_dat
            """
    ),

#rev_dat count


##############################
 
 # Rule 2

 # People for who Asthma quality indicator care was unsuitable in previous 12 months
    astpcapu=patients.with_these_clinical_events(
            codelist=astpcapu_cod,
            between=["last_day_of_month(index_date) - 365 days","last_day_of_month(index_date)"],
            returning="binary_flag",
            return_expectations={"incidence": 0.10},
        ),
##############################
 
 # Rule 3

# People who chose not to receive asthma monitoring in previous 12 months
    astmondec=patients.with_these_clinical_events(
            codelist=astmondec_cod,
            between=["last_day_of_month(index_date) - 365 days","last_day_of_month(index_date)"],
            returning="binary_flag",
            return_expectations={"incidence": 0.10},
    ),
##############################
 
 # Rule 4

# People who chose not to receive asthma quality indicator care in previous 12 months
    astpcadec=patients.with_these_clinical_events(
            codelist=astpcadec_cod,
            between=["last_day_of_month(index_date) - 365 days","last_day_of_month(index_date)"],
            returning="binary_flag",
            return_expectations={"incidence": 0.10},
    ),
##############################
 
 # Rule 5

#     # Latest asthma invite date
    astinvite_1=patients.with_these_clinical_events(
        codelist=astinvite_cod,
        returning="binary_flag",
        find_last_match_in_period=True,
        on_or_before="last_day_of_month(index_date)",
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
    ),
    # Latest asthma invite date 7 days before the last one
    astinvite_2=patients.with_these_clinical_events(
        codelist=astinvite_cod,
        returning="binary_flag",
        find_last_match_in_period=True,
        between=[
            "astinvite_1_date + 6 days",
            "last_day_of_month(index_date)",
        ],
    ),
##############################
 
 # Rule 6

 # Exclude people who were diagnosed with asthma in the last 3 months

    ast_diag_max_4_months=patients.with_these_clinical_events(
            ast_cod,
            on_or_before="first_day_of_month(index_date) - 2 months",
            returning='binary_flag',
            return_expectations={"incidence": 0.10},
        ),
##############################
 
 # Rule 7

# Reject patients passed to this rule who registered with the GP practice
# in the 3 month period leading up to and including the payment period end
# date. Select the remaining patients.
    registered_3mo=patients.registered_with_one_practice_between(
        start_date="first_day_of_month(index_date) - 2 months",
        end_date="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.1},
    ),
          
##############################          

ast007_denom=patients.satisfying(
    """
    ast007_rule1

    OR

    (
    NOT astpcapu AND 
    NOT astmondec AND
    NOT astpcadec AND
    (astinvite_1 AND astinvite_2) AND
    (ast_diag_max_4_months)
    )
    


    """
),




################################################################################################
    practice=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),

    region=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }}}
    ),
    
    imd=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "1 - Most deprived": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5 - Least deprived": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "last_day_of_month(index_date)",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Unknown": 0.05,
                    "1 - Most deprived": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5 - Least deprived": 0.19,
                }
            },
        },
    ),

    learning_disability=patients.with_these_clinical_events(
        ld_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        return_expectations={"incidence": 0.01, },
    ),
    
    care_home_status=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        on_or_before="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.2}
    )

)




# Create default measures
measures = [

    Measure(
        id="event_rate",
        numerator="ast_population",
        denominator="population",
        group_by="population",
        small_number_suppression=True
    ),

    # Measure(
    #     id="event_code_rate",
    #     numerator="ast_population",
    #     denominator="population",
    #     group_by=["event_code"],
    #     small_number_suppression=True
    # ),

    Measure(
        id="practice_rate",
        numerator="ast_population",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=True,
    ),


]


#Add demographics measures#
# Q - does this need to be included.

for d in demographics:

    # if d == ["imd", "age_band"]:
    #     apply_suppression = False
    
    # else:
    #     apply_suppression = True
    
    m = Measure(
        id=f'{d}_rate',
        numerator="ast_population",
        denominator="population",
        group_by=[d],
        small_number_suppression=True
    )
    
    measures.append(m)

    
