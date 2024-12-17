from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# Example data
data = [["the food is bad"]]

# Instantiate the OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)

# Fit and transform the input data
encoded_data = encoder.fit_transform(data)

# Display the encoded result in a DataFrame for better visualization
df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())
print(df)
