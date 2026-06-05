import os
import json

data_dir = 'd:/AI_VINUNI/LAB7/Day-07-Lab-Data-Foundations/data'
os.makedirs(data_dir, exist_ok=True)

docs = {
    'diabetes.md': """# Diabetes

## Definition
Diabetes is a chronic disease that affects how the body converts food into energy. The body either does not produce enough insulin or cannot use insulin effectively.

## Symptoms
- Increased thirst
- Frequent urination
- Increased hunger
- Fatigue
- Blurred vision
- Slow-healing wounds

## Causes / Risk Factors
- Genetic factors
- Obesity
- Physical inactivity
- Autoimmune destruction of insulin-producing cells (Type 1)

## Diagnosis
- Fasting Blood Glucose Test
- HbA1c Test
- Oral Glucose Tolerance Test

## Treatment
- Healthy diet
- Regular exercise
- Insulin therapy
- Oral medications

## Prevention
- Maintain healthy weight
- Regular physical activity
- Healthy eating habits
""",

    'diabetic_retinopathy.md': """# Diabetic Retinopathy

## Definition
Diabetic retinopathy is a diabetes complication that affects the eyes. It occurs when high blood sugar damages blood vessels in the retina.

## Symptoms
- Blurred vision
- Floaters
- Dark areas in vision
- Vision loss

## Risk Factors
- Long duration of diabetes
- Poor blood sugar control
- High blood pressure
- High cholesterol

## Diagnosis
- Dilated eye examination
- Retinal imaging
- Optical coherence tomography (OCT)

## Treatment
- Blood sugar control
- Laser treatment
- Anti-VEGF injections
- Vitrectomy surgery

## Prevention
- Control blood glucose levels
- Regular eye examinations
- Manage blood pressure
""",

    'asthma.md': """# Asthma

## Definition
Asthma is a chronic disease that affects the airways of the lungs.

## Symptoms
- Wheezing
- Shortness of breath
- Chest tightness
- Coughing

## Triggers / Risk Factors
- Allergens
- Smoke
- Air pollution
- Respiratory infections

## Diagnosis
- Physical examination
- Spirometry
- Peak flow measurement

## Treatment
- Inhaled corticosteroids
- Bronchodilators
- Avoidance of triggers

## Prevention
- Avoid smoking
- Reduce exposure to allergens
""",

    'hypertension.md': """# Hypertension

## Definition
Hypertension, or high blood pressure, is a condition where the force of the blood against the artery walls is too high.

## Symptoms
- Most people have no symptoms
- Headaches
- Shortness of breath
- Nosebleeds

## Causes / Risk Factors
- High sodium diet
- Lack of physical activity
- Obesity
- Stress
- Genetics

## Diagnosis
- Blood pressure measurement with a sphygmomanometer
- Blood tests
- Electrocardiogram (ECG)

## Treatment
- Lifestyle changes
- Diuretics
- ACE inhibitors
- Beta-blockers

## Prevention
- Reduce sodium intake
- Exercise regularly
- Limit alcohol
- Manage stress
""",

    'migraine.md': """# Migraine

## Definition
A migraine is a neurological condition that can cause multiple symptoms, frequently including intense, debilitating headaches.

## Symptoms
- Severe throbbing pain or a pulsing sensation, usually on one side of the head
- Nausea
- Vomiting
- Extreme sensitivity to light and sound

## Causes / Risk Factors
- Hormonal changes
- Stress
- Certain foods and drinks
- Changes in sleep patterns
- Genetics

## Diagnosis
- Neurological exam
- MRI or CT scan
- Medical history

## Treatment
- Pain-relieving medications
- Preventive medications
- Resting in a dark, quiet room

## Prevention
- Identify and avoid triggers
- Consistent sleep schedule
- Stress management
""",

    'breast_cancer.md': """# Breast Cancer

## Definition
Breast cancer is a disease in which cells in the breast grow out of control.

## Symptoms
- A lump in the breast or underarm
- Thickening or swelling of part of the breast
- Irritation or dimpling of breast skin
- Redness or flaky skin in the nipple area

## Causes / Risk Factors
- Genetics (BRCA1 and BRCA2 genes)
- Age
- Radiation exposure
- Obesity

## Diagnosis
- Mammogram
- Breast ultrasound
- Biopsy
- Breast magnetic resonance imaging (MRI)

## Treatment
- Surgery (Lumpectomy or Mastectomy)
- Radiation therapy
- Chemotherapy
- Hormone therapy

## Prevention
- Limit alcohol
- Maintain a healthy weight
- Be physically active
""",

    'lung_cancer.md': """# Lung Cancer

## Definition
Lung cancer is a type of cancer that begins in the lungs. It is the leading cause of cancer deaths worldwide.

## Symptoms
- A new cough that doesn't go away
- Coughing up blood
- Shortness of breath
- Chest pain
- Hoarseness

## Causes / Risk Factors
- Smoking
- Exposure to secondhand smoke
- Exposure to radon gas
- Asbestos and other carcinogens

## Diagnosis
- Imaging tests (X-ray, CT scan)
- Sputum cytology
- Tissue sample (Biopsy)

## Treatment
- Surgery
- Radiation therapy
- Chemotherapy
- Targeted drug therapy
- Immunotherapy

## Prevention
- Don't smoke
- Stop smoking
- Avoid secondhand smoke
- Test your home for radon
""",

    'glaucoma.md': """# Glaucoma

## Definition
Glaucoma is a group of eye conditions that damage the optic nerve, the health of which is vital for good vision. This damage is often caused by an abnormally high pressure in your eye.

## Symptoms
- Patchy blind spots in your side or central vision, frequently in both eyes
- Tunnel vision in the advanced stages
- Severe headache
- Eye pain
- Nausea and vomiting
- Blurred vision
- Halos around lights

## Causes / Risk Factors
- Elevated internal eye pressure
- Age (over 60)
- Being black, Asian, or Hispanic
- Family history of glaucoma
- Certain medical conditions, such as diabetes, heart disease, high blood pressure, and sickle cell anemia

## Diagnosis
- Tonometry (measuring inner eye pressure)
- Ophthalmoscopy (testing for optic nerve damage)
- Perimetry (visual field test)
- Gonioscopy (measuring the angle where the iris meets the cornea)
- Pachymetry (measuring cornea thickness)

## Treatment
- Eyedrops (prostaglandins, beta blockers)
- Oral medications
- Laser therapy (trabeculoplasty, iridotomy)
- Surgery (filtering surgery, drainage tubes)

## Prevention
- Get regular dilated eye examinations
- Know your family's eye health history
- Exercise safely
- Take prescribed eyedrops regularly
- Wear eye protection
""",

    'cataract.md': """# Cataract

## Definition
A cataract is a clouding of the normally clear lens of your eye. For people who have cataracts, seeing through cloudy lenses is a bit like looking through a frosty or fogged-up window.

## Symptoms
- Clouded, blurred or dim vision
- Increasing difficulty with vision at night
- Sensitivity to light and glare
- Need for brighter light for reading and other activities
- Seeing "halos" around lights
- Frequent changes in eyeglass or contact lens prescription
- Fading or yellowing of colors
- Double vision in a single eye

## Causes / Risk Factors
- Increasing age
- Diabetes
- Excessive exposure to sunlight
- Smoking
- Obesity
- High blood pressure
- Previous eye injury or inflammation
- Previous eye surgery
- Prolonged use of corticosteroid medications
- Drinking excessive amounts of alcohol

## Diagnosis
- Visual acuity test
- Slit-lamp examination
- Retinal exam
- Applanation tonometry (fluid pressure test)

## Treatment
- Prescription glasses for early stages
- Surgery (phacoemulsification, extracapsular cataract extraction)

## Prevention
- Have regular eye examinations
- Quit smoking
- Manage other health problems (e.g., diabetes)
- Choose a healthy diet that includes plenty of fruits and vegetables
- Wear sunglasses
- Reduce alcohol use
""",

    'osteoporosis.md': """# Osteoporosis

## Definition
Osteoporosis causes bones to become weak and brittle — so brittle that a fall or even mild stresses such as bending over or coughing can cause a fracture. Osteoporosis-related fractures most commonly occur in the hip, wrist or spine.

## Symptoms
- There typically are no symptoms in the early stages of bone loss. But once your bones have been weakened by osteoporosis, you might have signs and symptoms that include:
- Back pain, caused by a fractured or collapsed vertebra
- Loss of height over time
- A stooped posture
- A bone that breaks much more easily than expected

## Causes / Risk Factors
- Sex (women are much more likely to develop osteoporosis)
- Age (the older you get, the greater your risk)
- Race (greatest risk for white and Asian descent)
- Family history
- Body frame size (small body frames = higher risk)
- Hormone levels (low estrogen or testosterone, too much thyroid hormone)
- Dietary factors (low calcium intake, eating disorders, gastrointestinal surgery)

## Diagnosis
- Bone density test (DEXA scan)
- X-rays
- Ultrasound
- CT scans

## Treatment
- Bisphosphonates (Alendronate, Risedronate, Ibandronate, Zoledronic acid)
- Hormone-related therapy (Estrogen, Raloxifene)
- Bone-building medications (Teriparatide, Abaloparatide, Romosozumab)

## Prevention
- Good nutrition
- Regular exercise
- Calcium-rich diet
- Vitamin D
"""
}

for fname, content in docs.items():
    with open(os.path.join(data_dir, fname), 'w', encoding='utf-8') as f:
        f.write(content)

benchmark = [
  {
    "question": "What is diabetic retinopathy?",
    "expected_doc": "diabetic_retinopathy.md",
    "expected_answer": "Diabetic retinopathy is a diabetes complication affecting the retina."
  },
  {
    "question": "What are common symptoms of asthma?",
    "expected_doc": "asthma.md",
    "expected_answer": "Wheezing, shortness of breath, chest tightness, and coughing."
  },
  {
    "question": "How is diabetes diagnosed?",
    "expected_doc": "diabetes.md",
    "expected_answer": "Fasting blood glucose, HbA1c, and oral glucose tolerance tests."
  },
  {
    "question": "How can diabetic retinopathy be prevented?",
    "expected_doc": "diabetic_retinopathy.md",
    "expected_answer": "Control blood glucose and receive regular eye examinations."
  },
  {
    "question": "What treatments are available for asthma?",
    "expected_doc": "asthma.md",
    "expected_answer": "Inhaled corticosteroids and bronchodilators."
  }
]

with open(os.path.join(data_dir, 'benchmark_questions.json'), 'w', encoding='utf-8') as f:
    json.dump(benchmark, f, indent=2)

print("Files created successfully.")
