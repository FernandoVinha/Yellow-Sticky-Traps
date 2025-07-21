# Yellow Sticky Traps Dataset – A Practical Debugging Journey

## My Workflow and Lessons Learned

### 1. Download and First Inspection

After downloading the [Kaggle Yellow Sticky Traps dataset](https://www.kaggle.com/datasets/friso1987/yellow-sticky-traps/data), I started by **printing out a few images** to check the content and the annotation overlay.  
To do this, I wrote `print.py` to simply open and display each image.

Yellow-Sticky-Traps/images/1000_preview.jpg  quro colcoar a iamgem aqui

#### Key finding:
- Some images were in **portrait**, others in **landscape**.
- All XML annotation files assumed **landscape orientation**.
- When plotting bounding boxes on portrait images, **annotations were misaligned**.

### 2. The First Attempt at Fixing Rotation

Thinking the problem was only with portrait images, I tried to rotate all images by 90 degrees using a script (`print_90.py`).  
But this approach **didn’t solve the problem**—in fact, it broke the alignment for the landscape images! Now both types could end up mismatched with their annotations, depending on the original orientation.

Yellow-Sticky-Traps/images/1000_rotated_annotated.jpg   quero colcoar a iamgem aqui falndo que aqui falando que funcionou 



Yellow-Sticky-Traps/images/1170_rotated_annotated.jpg  e para esta não funcionou

#### Lesson:
- Rotating everything blindly is not enough.  
- The dataset contained **both portrait and landscape images**; only portrait images needed rotation.

### 3. The Final Fix: Smart Orientation Script

I developed `fix_dataset.py` to **automatically check the orientation of each image** and only rotate those in portrait mode (height > width).  
After running this, all images matched their respective annotation files, and bounding boxes aligned perfectly.

#### What the script does:
- Checks each image’s height and width.
- Rotates only those where height > width.
- Leaves landscape images unchanged.

### 4. Training and Further Insights

With the orientation fixed, I proceeded to train object detection models at different image resolutions (16MP, 5MP, and 2MP) to balance accuracy and efficiency for edge deployment.  
I also discovered that many insects in the dataset **weren’t annotated at all**, which resulted in false positives during evaluation.  
To further optimize for microcontroller usage, I later sliced images into small patches focused on annotated insects.

---

### 5. Final Step: Cropping to 120px Patches – Solving False Positives

After noticing that the model was still producing some false positives, I realized that the problem was partially due to large image areas with background and no insects.  
To address this, I implemented a **cropping strategy**: I split each image into 120x120 pixel patches and **kept only the patches that actually contained annotated insects**.

#### Result:
- The model now trained only on regions with real insects.
- This **significantly reduced false positives**, since the model was no longer exposed to large empty backgrounds or ambiguous areas.
- The pipeline also became much more suitable for deployment on microcontrollers and other edge devices, as each inference now happened on a small, focused patch.

---

## Workflow Summary

1. Download and inspect the data (`print.py`)
2. Try a blind rotation (didn't work) (`print_90.py`)
3. Fix orientation intelligently (`fix_dataset.py`)
4. Train models and analyze annotation quality
5. **Crop images to 120x120px patches containing insects to eliminate false positives**

## Included Scripts

- `print.py` — Initial inspection: print and view dataset images.
- `print_90.py` — Blind 90-degree rotation test (failed experiment).
- `fix_dataset.py` — Final script: rotate only portrait images.
- (Others: cropping, training, etc. as your pipeline evolved.)

---

## Lessons for Others

- **Always inspect a dataset visually before training.**
- **Never assume annotations are perfect or that all images share the same orientation.**
- **Try, test, and validate every preprocessing step, not just theoretically, but by visualizing the result.**
- **Smart, targeted preprocessing beats “one-size-fits-all” fixes every time.**

---

## Contact

For questions, improvements, or if you want to share experiences with similar datasets:  
[your email or GitHub]

---


### 3. The Final Fix: Smart Orientation Script

I developed `fix_dataset.py` to **automatically check the orientation of each image** and only rotate those in portrait mode (height > width).  
After running this, all images matched their respective annotation files, and bounding boxes aligned perfectly.

#### What the script does:
- Checks each image’s height and width.
- Rotates only those where height > width.
- Leaves landscape images unchanged.

### 4. Training and Further Insights

With the orientation fixed, I proceeded to train object detection models at different image resolutions (16MP, 5MP, and 2MP) to balance accuracy and efficiency for edge deployment.  
I also discovered that many insects in the dataset **weren’t annotated at all**, which resulted in false positives during evaluation.  
To further optimize for microcontroller usage, I later sliced images into small patches focused on annotated insects.

---

### 5. Final Step: Cropping to 120px Patches – Solving False Positives

After noticing that the model was still producing some false positives, I realized that the problem was partially due to large image areas with background and no insects.  
To address this, I implemented a **cropping strategy**: I split each image into 120x120 pixel patches and **kept only the patches that actually contained annotated insects**.

#### Result:
- The model now trained only on regions with real insects.
- This **significantly reduced false positives**, since the model was no longer exposed to large empty backgrounds or ambiguous areas.
- The pipeline also became much more suitable for deployment on microcontrollers and other edge devices, as each inference now happened on a small, focused patch.

---

## Workflow Summary

1. Download and inspect the data (`print.py`)
2. Try a blind rotation (didn't work) (`print_90.py`)
3. Fix orientation intelligently (`fix_dataset.py`)
4. Train models and analyze annotation quality
5. **Crop images to 120x120px patches containing insects to eliminate false positives**

## Included Scripts

- `print.py` — Initial inspection: print and view dataset images.
- `print_90.py` — Blind 90-degree rotation test (failed experiment).
- `fix_dataset.py` — Final script: rotate only portrait images.
- (Others: cropping, training, etc. as your pipeline evolved.)

---

## Lessons for Others

- **Always inspect a dataset visually before training.**
- **Never assume annotations are perfect or that all images share the same orientation.**
- **Try, test, and validate every preprocessing step, not just theoretically, but by visualizing the result.**
- **Smart, targeted preprocessing beats “one-size-fits-all” fixes every time.**

---

## Contact

For questions, improvements, or if you want to share experiences with similar datasets:  
[your email or GitHub]

---

