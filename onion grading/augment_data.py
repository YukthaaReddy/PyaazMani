import cv2
import os
import albumentations as A


IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png"
)


transform = A.Compose([

    A.HorizontalFlip(
        p=0.5
    ),

    A.Rotate(
        limit=25,
        p=0.6
    ),

    A.RandomBrightnessContrast(
        brightness_limit=0.20,
        contrast_limit=0.20,
        p=0.5
    ),

    A.GaussNoise(
        p=0.2
    ),

    A.OneOf([

        A.MotionBlur(
            blur_limit=3
        ),

        A.MedianBlur(
            blur_limit=3
        ),

    ], p=0.15),

    A.ShiftScaleRotate(

        shift_limit=0.05,

        scale_limit=0.10,

        rotate_limit=10,

        p=0.4

    )

])


def augment_folder(
    folder,
    target_count=100
):

    if not os.path.exists(folder):

        print(
            f"Folder not found: {folder}"
        )

        return


    original_files = [

        f

        for f in os.listdir(folder)

        if f.lower().endswith(
            IMAGE_EXTENSIONS
        )

        and not f.startswith("aug_")

    ]


    if not original_files:

        print(
            f"No images found in {folder}"
        )

        return


    existing_files = [

        f

        for f in os.listdir(folder)

        if f.lower().endswith(
            IMAGE_EXTENSIONS
        )

    ]


    current_count = len(
        existing_files
    )


    print(
        f"{folder}: "
        f"{current_count} images"
    )


    counter = 0


    while current_count < target_count:

        source_name = original_files[
            counter % len(original_files)
        ]

        source_path = os.path.join(
            folder,
            source_name
        )


        image = cv2.imread(
            source_path
        )


        if image is None:

            counter += 1

            continue


        augmented = transform(
            image=image
        )["image"]


        filename = (
            f"aug_{counter}_"
            f"{source_name}"
        )


        output_path = os.path.join(
            folder,
            filename
        )


        cv2.imwrite(
            output_path,
            augmented
        )


        current_count += 1
        counter += 1


    print(
        f"Completed: {folder}"
    )


# --------------------------------------------------
# RUN
# --------------------------------------------------

for grade in [

    "grade_A",
    "grade_B",
    "grade_C"

]:

    augment_folder(
        f"data/{grade}",
        target_count=100
    )