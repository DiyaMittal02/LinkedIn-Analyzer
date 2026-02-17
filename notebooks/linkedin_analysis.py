# ==========================================
# LINKEDIN JOB MARKET ANALYSIS - FULL SCRIPT
# ==========================================

import pandas as pd
import numpy as np

print("Starting Data Pipeline...\n")

# ------------------------------------------------
# 1️⃣ LOAD ALL DATA (IMPORTANT: ../data PATH)
# ------------------------------------------------

posting = pd.read_csv("../data/postings.csv")

companies = pd.read_csv("../data/companies/companies.csv")
company_industries = pd.read_csv("../data/companies/company_industries.csv")
employee_counts = pd.read_csv("../data/companies/employee_counts.csv")

job_industries = pd.read_csv("../data/jobs/job_industries.csv")
job_skills = pd.read_csv("../data/jobs/job_skills.csv")

industries = pd.read_csv("../data/mappings/industries.csv")
skills = pd.read_csv("../data/mappings/skills.csv")

print("All datasets loaded successfully ✅\n")

# ------------------------------------------------
# 2️⃣ CLEAN COLUMN NAMES (VERY IMPORTANT)
# ------------------------------------------------

def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

posting = clean_columns(posting)
companies = clean_columns(companies)
company_industries = clean_columns(company_industries)
employee_counts = clean_columns(employee_counts)
job_industries = clean_columns(job_industries)
job_skills = clean_columns(job_skills)
industries = clean_columns(industries)
skills = clean_columns(skills)

print("Column names standardized ✅\n")

# ------------------------------------------------
# 3️⃣ MERGE COMPANY BASIC INFO
# ------------------------------------------------

df = posting.merge(companies, on="company_id", how="left")

if "company_id" in employee_counts.columns:
    df = df.merge(employee_counts, on="company_id", how="left")

print("Company data merged ✅\n")

# ------------------------------------------------
# 4️⃣ CORRECT INDUSTRY MERGE (FIXED)
# ------------------------------------------------

# Convert both to string to avoid dtype mismatch
company_industries["industry"] = company_industries["industry"].astype(str)
industries["industry_id"] = industries["industry_id"].astype(str)

print("Merging company_industries.industry with industries.industry_id\n")

company_industry_full = company_industries.merge(
    industries,
    left_on="industry",
    right_on="industry_id",
    how="left"
)

# Merge industry name into main dataframe
df = df.merge(
    company_industry_full[["company_id", "industry_name"]],
    on="company_id",
    how="left"
)

print("Industry merge successful ✅\n")

# ------------------------------------------------
# 5️⃣ MERGE JOB SKILLS
# ------------------------------------------------

# Detect keys
skill_left = None
skill_right = None

for col in job_skills.columns:
    if "skill" in col:
        skill_left = col
        break

for col in skills.columns:
    if "skill" in col or col == "id":
        skill_right = col
        break

if skill_left and skill_right:
    print(f"Merging skills using {skill_left} and {skill_right}\n")

    job_skill_full = job_skills.merge(
        skills,
        left_on=skill_left,
        right_on=skill_right,
        how="left"
    )

    if "job_id" in job_skill_full.columns:
        df = df.merge(
            job_skill_full,
            on="job_id",
            how="left"
        )

        print("Skills merged successfully ✅\n")

# ------------------------------------------------
# 6️⃣ SALARY NORMALIZATION
# ------------------------------------------------

salary_cols = ["min_salary", "max_salary", "med_salary"]

for col in salary_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

def normalize_salary(row):
    if "pay_period" not in df.columns:
        return row.get("med_salary", np.nan)

    if row["pay_period"] == "HOURLY":
        return row["med_salary"] * 40 * 52
    elif row["pay_period"] == "MONTHLY":
        return row["med_salary"] * 12
    elif row["pay_period"] == "WEEKLY":
        return row["med_salary"] * 52
    else:
        return row["med_salary"]

if "med_salary" in df.columns:
    df["normalized_salary"] = df.apply(normalize_salary, axis=1)

print("Salary normalization complete ✅\n")

# ------------------------------------------------
# 7️⃣ EXPORT CLEAN FILE FOR TABLEAU
# ------------------------------------------------

export_cols = [
    col for col in df.columns
    if col in [
        "job_id", "company_name", "title",
        "location", "normalized_salary",
        "experience_level", "views"
    ]
]

df_final = df[export_cols].drop_duplicates()

df_final.to_csv("../final_cleaned_jobs.csv", index=False)

print("Final dataset exported as: final_cleaned_jobs.csv ✅")
print("\n🚀 DATA PIPELINE COMPLETED SUCCESSFULLY 🚀")
