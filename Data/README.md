# README for [Original B2P Dataset](https://github.com/Lambda-School-Labs/bridges-to-prosperity-ds-e/blob/main/Data/B2P_original_dataset.csv)

# Instructions:
## Problem 1: Parsing 2013/2014 needs assessment data into current fields

300+ sites were initially identified as part of an informal needs assessment conducted by our Rwanda field staff over 2013 and 2014. We collected much of the same data that we do now, but in a less structured format. When we created the database in 2017, we loaded all the old needs assessment into the general comments field on each bridge record (column `Bridge Opportunity: Comments` in this table), just to keep as a reference. We now believe that loading this data into our standard project assessments would be a benefit to future needs assessment work, both field-based and remote. We would love to see the needs assessment data from `Bridge Opportunity: Comments` parsed into the corresponding columns after it (M+), with a new row if there is existing data in those columns. If no corresponding column is obvious, we'd like to see new columns created for any extraneous data that is common to the old format. 


## Problem 2: Predicting which sites will be technically rejected in future engineering reviews

Any sites with a "Yes" in the column `Senior Engineering Review Conducted` have undergone a full technical review, and of those, the Stage (`Bridge Opportunity: Stage`) can be considered to be correct. Any sites without a "Yes" in Column `Senior Engineering Review Conducted` have not undergone a full technical review, and the Stage is based on the assessor's initial estimate as to whether the site was technically feasible or not. We want to know if we can use the sites that have been reviewed to understand which of the sites that haven't yet been reviewed are likely to be rejected by the senior engineering team. Any of the data can be used, but our guess is that Estimated Span, Height Differential Between Banks, Created By, and Flag for Rejection are likely to be the most reliable predictors. 


-------------------------------------------------------------------



# Data Dictionary
| Field | Description |
| --- | ----------- |
| Bridge Name | nan |
| Bridge Opportunity: Project Code | Unique ID |
| Bridge Opportunity: Needs Assessment | This will be populated with "Rwanda 2018 Needs Assessment" if this was included in the formal needs assessment conducted in 2018 |
| Bridge Opportunity: Level 1 Government | Province |
| Bridge Opportunity: Level 2 Government | District |
| Bridge Opportunity: Stage | Project status of this site as of 2020.10.26 |
| Bridge Opportunity: GPS (Latitude) | nan |
| Bridge Opportunity: GPS (Longitude) | nan |
| Bridge Opportunity: Bridge Type | Type of standard bridge built or recommended |
| Bridge Opportunity: Span (m) | The length of the bridge as determined by senior engineers |
| Bridge Opportunity: Individuals Directly Served | nan |
| Bridge Opportunity: Project Narrative | nan |
| Bridge Opportunity: Comments | This field contains the data from the 2013/2014 informal needs assessment; if this field does not have contents that look like needs assessment data, it was not included in that assessment |
| Form: Form Name | All data from this column on was a part of the 2018 needs assessment form submitted by the assessment team |
| Form: Created By | Assessor that conducted the project assessment in 2018 |
| Proposed Bridge Location (GPS) (Latitude) | The initial proposed coordinates |
| Proposed Bridge Location (GPS) (Longitude) | The initial proposed coordinates |
| Current crossing method | Description of the community crossed pre-bridge |
| Nearest all-weather crossing point | Nearest place people can cross the river safely  |
| Days per year river is flooded | nan |
| Flood duration during rainy season | nan |
| Market access blocked by river | nan |
| Education access blocked by river | nan |
| Health access blocked by river | nan |
| Other access blocked by river | nan |
| Primary occupations | nan |
| Primary crops grown | nan |
| River crossing deaths in last 3 years | nan |
| River crossing injuries in last 3 years | nan |
| Incident descriptions | nan |
| Notes on social information | nan |
| Cell service quality | nan |
| 4WD Accessibility | How much of the year the path to the site is accessible by a four-wheel drive vehicle |
| Name of nearest city | nan |
| Name of nearest paved or sealed road | nan |
| Bridge classification | Assessor's estimate of whether a bridge at the location would be a standard design or not |
| Flag for Rejection | Assessor's estimate of whether or not the bridge should be rejected for immediate construction, usually on the basis of technical feasibility |
| Rejection Reason | Reason the site was flagged for rejection, if applicable |
| Bridge Type | Assessor's estimate of what type of bridge would be the best fit |
| Estimated span (m) | Assessor's estimate of the bridge length |
| Height differential between banks | nan |
| Bridge Opportunity: General Project Photos | Link to Flickr photo album, if applicable |
| Bridge Opportunity: CaseSafeID | Unique ID for dataloading to Salesforce  |
| Senior Engineering Review Conducted | nan |
| 4WD Accessibility | How much of the year the path to the site is accessible by a four-wheel drive vehicle |
| Name of nearest city | nan |
| Name of nearest paved or sealed road | nan |
| Bridge classification | Assessor's estimate of whether a bridge at the location would be a standard design or not |
| Flag for Rejection | Assessor's estimate of whether or not the bridge should be rejected for immediate construction, usually on the basis of technical feasibility |
| Rejection Reason | Reason the site was flagged for rejection, if applicable |
| Bridge Type | Assessor's estimate of what type of bridge would be the best fit |
| Estimated span (m) | Assessor's estimate of the bridge length |
| Height differential between banks | nan |
| Bridge Opportunity: General Project Photos | Link to Flickr photo album, if applicable |
| Bridge Opportunity: CaseSafeID | Unique ID for dataloading to Salesforce  |
| Senior Engineering Review Conducted | nan |
