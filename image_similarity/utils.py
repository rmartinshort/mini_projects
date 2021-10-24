
import pandas as pd
import matplotlib.pyplot as plt

def show_image(image_path, title=None):
    pp = plt.imread(image_path)
    plt.imshow(pp)
    plt.axis("off")
    if title:
        plt.title(title)
    plt.show()


def show_matched_result(match_df, metadata=None):
    if isinstance(metadata, pd.DataFrame):
        match_df["creative_id"] = match_df["match"]. \
            apply(lambda x: str(x.split("/")[-1].split("_")[1].split(".")[0]))
        match_df = match_df.merge(metadata, on="creative_id")

    for i, match in match_df.iterrows():
        image = match["match"]
        if isinstance(metadata, pd.DataFrame):
            country = match["country"]
            app_name = match["app_name"]
            image_title = "Creative from {} shown in {}".format(app_name, country)
            show_image(image, image_title)
        else:
            show_image(image)
        print("-----------------------------------\n")