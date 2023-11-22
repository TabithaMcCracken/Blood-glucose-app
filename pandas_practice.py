import pandas as pd

# df = pd.DataFrame(
#     {
#         "Name": [
#             "Braund, Mr. Owen Harris",
#             "Allen, Mr. William Henry",
#             "Bonnell, Miss. Elizabeth",
#         ],
#         "Age": [22, 35, 58],
#         "Sex": ["male", "male", "female"],
#     }
# )
# print(df["Age"])

# ages = pd.Series([22, 35, 58], name="Age")

# print(ages)

# print(df["Age"].max())
# print(df.describe())

file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_day.csv"
glucose = pd.read_csv(f"{file_path}")
print(glucose.head(8))
print(glucose.dtypes)