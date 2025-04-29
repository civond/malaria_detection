import numpy as np
import cv2
import os
import pandas as pd

def resize_image(df, raw_path, input_dimensions):
    for _, row in df.iterrows():
        img_id = row['id']
        img_write_path = row['path']
        img_read_path = os.path.join(raw_path, img_id)
    
        if os.path.isfile(img_write_path) == False:
            img = cv2.imread(img_read_path)
            resized_img = cv2.resize(img, (input_dimensions[0], input_dimensions[1])) # Change according to input dimensions of model used
            cv2.imwrite(img_write_path, resized_img)

            print(f"\tResizing: {img_read_path}")

        else:
            print(f"{img_write_path} already exists. Skipping...")
            pass


def main():
    csv_path = "./data/Train.csv"   # Csv path
    raw_path = "./data/images/"     # File location
    train_path = "./data/train/"    # Train directory
    test_path = "./data/test/"      # Test directory

    df = pd.read_csv(csv_path)
    ids = df['Image_ID'].unique()
    has_trophozoite = np.ones(len(ids)) # Preallocate label vector

    # Filter dataset for unique image id
    for idx, unique_id in enumerate(ids):
        temp_df = df[df["Image_ID"] == unique_id]
        has_trophozoite[idx] = int((temp_df['class'] == 'Trophozoite').any()) # Checks for trophozoites (0: neg, 1: positive)

    # Create temp dataframe
    df_temp = pd.DataFrame({
        "id": ids,
        "label": has_trophozoite
    })

    df_temp['label'] = df_temp['label'].astype(int) # Convert float to int

    paths = []
    for _, row in df_temp.iterrows():
        id = row['id']  # full path to file
        label = row['label']     # 0 or 1 (whatever your labels are)
        
        # No trophozoite
        if label == 0:
            temp_path = os.path.join(train_path, 'negative/', id)
        # Trophozoite
        else:
            temp_path = os.path.join(train_path, 'malaria/', id)
        paths.append(temp_path)

    new_df = pd.DataFrame({
        "id": ids,
        "path": paths,
        "label": has_trophozoite
    })
    new_df['label'] = new_df['label'].astype(int)
    new_df.to_csv('data.csv', index=False)

    # Resize the images contained in dataframe
    resize_image(new_df, 
                 raw_path, 
                 [300,300])
    print(new_df)
    
if __name__ == "__main__":
    main()

