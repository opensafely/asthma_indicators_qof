from cohortextractor import codelist_from_csv, combine_codelists
from config import codelist_path

# Change the path of the codelist to your chosen codelist
codelist = codelist_from_csv(codelist_path, system='snomed')

ast_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ast_cod.csv",
    system="snomed",
    column="code",
)

asttrt_cod = codelist_from_csv(
    "codelists/opensafely-asthma-related-drug-treatment-codes.csv",
    system="snomed",
    column="code",
)

astres_cod= codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astres_cod.csv",
    system="snomed",
    column="code",
)

rev_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-rev_cod.csv",
    system="snomed",
    column="code",
)

writpastp_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-writpastp_cod.csv",
    system="snomed",
    column="code",
)

astcontass_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astcontass_cod.csv",
    system="snomed",
    column="code",
)

astexacb_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astexacb_cod.csv",
    system="snomed",
    column="code",
)

astpcapu_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astpcapu_cod.csv",
    system="snomed",
    column="code",
)

astmondec_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astmondec_cod.csv",
    system="snomed",
    column="code",
)

astpcadec_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astpcadec_cod.csv",
    system="snomed",
    column="code",
)

astinvite_cod=codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-astinvite_cod.csv",
    system="snomed",
    column="code",
)