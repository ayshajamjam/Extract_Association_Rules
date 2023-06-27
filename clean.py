import pandas as pd

file_name = "Popular_Baby_Names.csv"
file_name_output = "INTEGRATED-DATASET.csv"

# Read in original file (includes rank)
df = pd.read_csv(file_name)

# Remove all duplicate rows
df.drop_duplicates(subset=["Year of Birth", "Gender", "Ethnicity", "Child's First Name", "Count"], inplace=True)

# Drop rows with rank < 50
df = df[df['Rank'] <= 50]

# Drop rank column
df = df.drop('Rank', axis=1)

# Iterate through each row
for x in df.index:

    # Lowercase all names
    df.loc[x, "Child's First Name"] = df.loc[x, "Child's First Name"].lower()

    # Lowercase all genders
    df.loc[x, "Gender"] = df.loc[x, "Gender"].lower()

    # consolidate all ethnicities ('asian and paci' --> 'asian and pacific islander')
    df.loc[x, "Ethnicity"] = df.loc[x, "Ethnicity"].lower()
    if(df.loc[x, "Ethnicity"] == "white non hisp"):
        df.loc[x, "Ethnicity"]  = "asian and pacific islander"
    elif(df.loc[x, "Ethnicity"] == "asian and paci"):
        df.loc[x, "Ethnicity"] = "white non hispanic"
    elif(df.loc[x, "Ethnicity"] == "black non hisp"):
        df.loc[x, "Ethnicity"] = "black non hispanic"

# Push changes to file
df.to_csv(file_name_output, index=False)

def main():
    print("Hi")

if __name__=="__main__":
    main()