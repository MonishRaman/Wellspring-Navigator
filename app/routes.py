import csv
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

# List of symptoms to ask
SYMPTOMS = [
    "Fever",
    "Headache",
    "Cold",
    "Cough",
    "Sore Throat",
    "Runny Nose",
    "Sneezing",
    "Body Pain",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Abdominal Pain",
    "Bloating",
    "Heartburn",
    "Rash",
    "Chills",
    "Sweating",
    "Shortness of Breath",
    "Chest Pain",
    "Chest Discomfort",
    "Chest Tightness",
    "Wheezing",
    "Pain Swallowing",
    "Swollen Tonsils",
    "Painful Urination",
    "Frequent Urination",
    "Weight Loss",
    "Night Sweats",
    "Jaundice",
    "Swollen Lymph Nodes",
    "Loss of Taste or Smell",
    "Sensitivity to Light",
    "Sensitivity to Sound",
    "Redness in Eye",
    "Itchy Eyes",
    "Itching",
    "Burning Sensation",
    "Joint Pain",
    "Dizziness",
    "Rapid Heartbeat",
    "Numbness and Tingling",
    "Weakness",
    "Persistent Sadness",
    "Loss of Interest",
    "Changes in Appetite or Sleep",
    "Flashbacks",
    "Nightmares",
    "Swollen Salivary Glands",
    "Burning Stomach Pain",
    "Regurgitation",
    "itchy rash with blisters",
]

VALID_SYMPTOMS = set(SYMPTOMS)

def validate_responses(responses):
    return all(symptom in VALID_SYMPTOMS for symptom in responses.keys())

# Disease data: symptoms, description, and treatment
DISEASES = {
    "Common Cold": {"symptoms": {"Cold": 1, "Headache": 1, "Fatigue": 1, "Body Pain": 1}, "description": "A common viral infection of the upper respiratory tract.", "treatment": "Rest, fluids, over-the-counter symptom relief."},
    "Influenza (Flu)": {"symptoms": {"Fever": 1, "Headache": 1, "Fatigue": 1, "Body Pain": 1, "Cold": 1}, "description": "A contagious respiratory illness caused by influenza viruses.", "treatment": "Rest, fluids, antiviral medications (if prescribed early)."},
    "COVID-19": {"symptoms": {"Fever": 1, "Cough": 1, "Fatigue": 1, "Body Pain": 1, "Loss of Taste or Smell": 1}, "description": "A contagious respiratory illness caused by the SARS-CoV-2 virus.", "treatment": "Varies depending on severity; rest, fluids, antiviral medications, and supportive care."},
    "Allergies": {"symptoms": {"Sneezing": 1, "Runny Nose": 1, "Itchy Eyes": 1, "Rash": 1}, "description": "Hypersensitivity reactions of the immune system to typically harmless substances.", "treatment": "Avoidance of allergens, antihistamines, corticosteroids."},
    "Asthma": {"symptoms": {"Wheezing": 1, "Shortness of Breath": 1, "Cough": 1, "Chest Tightness": 1}, "description": "A chronic respiratory disease characterized by inflammation and narrowing of the airways.", "treatment": "Inhalers (bronchodilators and corticosteroids), avoidance of triggers."},
    "Bronchitis": {"symptoms": {"Cough": 1, "Fatigue": 1, "Shortness of Breath": 1, "Chest Discomfort": 1}, "description": "Inflammation of the bronchial tubes.", "treatment": "Rest, fluids, cough suppressants; antibiotics if bacterial."},
    "Pneumonia": {"symptoms": {"Cough": 1, "Fever": 1, "Chills": 1, "Shortness of Breath": 1, "Chest Pain": 1}, "description": "Infection of the air sacs in one or both lungs.", "treatment": "Antibiotics (if bacterial), antiviral medications (if viral), supportive care."},
    "Sinusitis": {"symptoms": {"Headache": 1, "Facial Pain": 1, "Nasal Congestion": 1, "Runny Nose": 1}, "description": "Inflammation of the sinuses.", "treatment": "Decongestants, saline nasal sprays, antibiotics if bacterial."},
    "Strep Throat": {"symptoms": {"Sore Throat": 1, "Fever": 1, "Pain Swallowing": 1}, "description": "A bacterial infection of the throat and tonsils.", "treatment": "Antibiotics."},
    "Tonsillitis": {"symptoms": {"Sore Throat": 1, "Fever": 1, "Pain Swallowing": 1, "Swollen Tonsils": 1}, "description": "Inflammation of the tonsils.", "treatment": "Rest, fluids, pain relievers; antibiotics if bacterial."},
    "Urinary Tract Infection (UTI)": {"symptoms": {"Painful Urination": 1, "Frequent Urination": 1, "Urgency to Urinate": 1}, "description": "An infection in any part of the urinary system.", "treatment": "Antibiotics."},
    "Kidney Stones": {"symptoms": {"Severe Flank Pain": 1, "Pain Radiating to Groin": 1, "Nausea": 1, "Vomiting": 1}, "description": "Hard deposits made of minerals and salts that form inside the kidneys.", "treatment": "Pain relievers, increased fluids, medical procedures in some cases."},
    "Gastroenteritis (Stomach Flu)": {"symptoms": {"Nausea": 1, "Vomiting": 1, "Diarrhea": 1, "Abdominal Cramps": 1}, "description": "Inflammation of the stomach and intestines, usually caused by a viral or bacterial infection.", "treatment": "Rest, fluids, bland diet."},
    "Food Poisoning": {"symptoms": {"Nausea": 1, "Vomiting": 1, "Diarrhea": 1, "Abdominal Pain": 1}, "description": "Illness caused by consuming contaminated food.", "treatment": "Rest, fluids, may resolve on its own."},
    "Appendicitis": {"symptoms": {"Severe Abdominal Pain (usually lower right)": 1, "Nausea": 1, "Vomiting": 1, "Fever": 1}, "description": "Inflammation of the appendix.", "treatment": "Surgical removal of the appendix."},
    "Peptic Ulcer": {"symptoms": {"Burning Stomach Pain": 1, "Bloating": 1, "Heartburn": 1}, "description": "Sores that develop on the lining of the stomach, esophagus, or small intestine.", "treatment": "Medications to reduce stomach acid, antibiotics if H. pylori infection is present."},
    "Acid Reflux (GERD)": {"symptoms": {"Heartburn": 1, "Regurgitation": 1}, "description": "Stomach acid backs up into the esophagus.", "treatment": "Lifestyle changes, antacids, medications to reduce acid production."},
    "Irritable Bowel Syndrome (IBS)": {"symptoms": {"Abdominal Pain": 1, "Bloating": 1, "Changes in Bowel Habits": 1}, "description": "A common disorder that affects the large intestine.", "treatment": "Dietary changes, stress management, medications to manage symptoms."},
    "Headache (Tension)": {"symptoms": {"Dull, Aching Head Pain": 1, "Tightness or Pressure Across Forehead or Sides of Head": 1}, "description": "The most common type of headache.", "treatment": "Over-the-counter pain relievers, stress management."},
    "Migraine": {"symptoms": {"Severe Throbbing Headache (often one-sided)": 1, "Nausea": 1, "Vomiting": 1, "Sensitivity to Light and Sound": 1}, "description": "A neurological condition that can cause intense headaches.", "treatment": "Pain relievers, triptans, preventive medications."},
    "Anemia": {"symptoms": {"Fatigue": 1, "Weakness": 1, "Pale Skin": 1, "Shortness of Breath": 1}, "description": "A condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.", "treatment": "Iron supplements, vitamin B12 or folate supplements, addressing underlying cause."},
    "Diabetes (Type 2)": {"symptoms": {"Increased Thirst": 1, "Frequent Urination": 1, "Increased Hunger": 1, "Fatigue": 1}, "description": "A chronic metabolic disorder characterized by high blood sugar.", "treatment": "Lifestyle changes (diet and exercise), oral medications, insulin injections."},
    "Hypertension (High Blood Pressure)": {"symptoms": {"Often no symptoms initially": 1, "Severe headache, chest pain, shortness of breath (in severe cases)": 1}, "description": "A condition in which the force of the blood against the artery walls is too high.", "treatment": "Lifestyle changes (diet and exercise), medications."},
    "Hypothyroidism": {"symptoms": {"Fatigue": 1, "Weight Gain": 1, "Feeling Cold": 1, "Dry Skin": 1}, "description": "A condition in which the thyroid gland doesn't produce enough thyroid hormone.", "treatment": "Thyroid hormone replacement medication."},
    "Hyperthyroidism": {"symptoms": {"Weight Loss": 1, "Rapid Heartbeat": 1, "Sweating": 1, "Anxiety": 1}, "description": "A condition in which the thyroid gland produces too much thyroid hormone.", "treatment": "Medications, radioactive iodine therapy, surgery."},
    "Arthritis (Osteoarthritis)": {"symptoms": {"Joint Pain": 1, "Stiffness": 1, "Decreased Range of Motion": 1}, "description": "A degenerative joint disease.", "treatment": "Pain relievers, anti-inflammatory medications, physical therapy, joint replacement surgery in severe cases."},
    "Arthritis (Rheumatoid)": {"symptoms": {"Joint Pain": 1, "Swelling": 1, "Stiffness (especially in the morning)": 1, "Fatigue": 1}, "description": "An autoimmune disease that attacks the joints.", "treatment": "Disease-modifying antirheumatic drugs (DMARDs), biologic agents, pain relievers."},
    "Gout": {"symptoms": {"Sudden, Severe Pain in a Joint (often the big toe)": 1, "Redness": 1, "Swelling": 1, "Warmth": 1}, "description": "A type of arthritis caused by a buildup of uric acid crystals in the joints.", "treatment": "Medications to reduce uric acid levels, anti-inflammatory drugs for acute attacks."},
    "Osteoporosis": {"symptoms": {"Often no symptoms until a fracture occurs": 1, "Back pain, loss of height, stooped posture": 1}, "description": "A condition in which bones become weak and brittle.", "treatment": "Calcium and vitamin D supplements, medications to increase bone density."},
    "Carpal Tunnel Syndrome": {"symptoms": {"Numbness and Tingling in Hand and Fingers": 1, "Weakness in Grip": 1}, "description": "A condition caused by compression of the median nerve in the wrist.", "treatment": "Wrist splints, corticosteroid injections, surgery in some cases."},
    "Sciatica": {"symptoms": {"Pain that Radiates from Lower Back Down the Leg": 1, "Numbness or Weakness in the Leg or Foot": 1}, "description": "Pain caused by irritation or compression of the sciatic nerve.", "treatment": "Pain relievers, physical therapy, injections, surgery in severe cases."},
    "Conjunctivitis (Pinkeye)": {"symptoms": {"Redness in the White of the Eye": 1, "Itching or Gritty Feeling": 1, "Discharge from the Eye": 1}, "description": "Inflammation or infection of the outer membrane of the eyeball and the inner eyelid.", "treatment": "Often resolves on its own; antibiotic eye drops if bacterial."},
    "Eczema (Atopic Dermatitis)": {"symptoms": {"Dry, Itchy Skin": 1, "Rash": 1, "Thickened, Cracked Skin": 1}, "description": "A chronic inflammatory skin condition.", "treatment": "Moisturizers, topical corticosteroids, antihistamines."},
    "Psoriasis": {"symptoms": {"Patches of Thick, Red Skin with Silvery Scales": 1, "Itching": 1, "Burning": 1}, "description": "A chronic autoimmune skin disease.", "treatment": "Topical treatments, phototherapy, systemic medications."},
    "Shingles (Herpes Zoster)": {"symptoms": {"Painful Rash with Blisters (usually on one side of the body)": 1, "Burning or Tingling Sensation": 1}, "description": "A reactivation of the varicella-zoster virus (chickenpox virus).", "treatment": "Antiviral medications, pain relievers."},
    "Lyme Disease": {"symptoms": {"Rash (often a bull's-eye shape)": 1, "Fever": 1, "Fatigue": 1, "Joint Pain": 1}, "description": "An infectious disease caused by bacteria transmitted by ticks.", "treatment": "Antibiotics."},
    "Measles": {"symptoms": {"Fever": 1, "Runny Nose": 1, "Cough": 1, "Rash (starts on face and spreads)": 1}, "description": "A highly contagious viral infection.", "treatment": "Rest, fluids, supportive care; vaccination is preventative."},
    "Mumps": {"symptoms": {"Swollen Salivary Glands (especially near the jaw)": 1, "Fever": 1, "Headache": 1}, "description": "A contagious viral infection that affects the salivary glands.", "treatment": "Rest, fluids, pain relievers; vaccination is preventative."},
    "Rubella (German Measles)": {"symptoms": {"Mild Fever": 1, "Rash": 1, "Swollen Lymph Nodes": 1}, "description": "A mild viral infection that can be serious in pregnant women.", "treatment": "Rest, fluids, supportive care; vaccination is preventative."},
    "Chickenpox": {"symptoms": {"Itchy Rash with Blisters": 1, "Fever": 1, "Fatigue": 1}, "description": "A highly contagious viral infection.", "treatment": "Calamine lotion, oatmeal baths, rest; vaccination is preventative."},
    "Hepatitis A": {"symptoms": {"Fatigue": 1, "Nausea": 1, "Vomiting": 1, "Jaundice (yellowing of skin and eyes)": 1}, "description": "A viral infection that affects the liver.", "treatment": "Rest, fluids, supportive care; vaccination is preventative."},
    "Hepatitis B": {"symptoms": {"Fatigue": 1, "Nausea": 1, "Vomiting": 1, "Jaundice (yellowing of skin and eyes)": 1}, "description": "A viral infection that affects the liver.", "treatment": "Antiviral medications; vaccination is preventative."},
    "Hepatitis C": {"symptoms": {"Often no symptoms initially": 1, "Fatigue, jaundice (in later stages)": 1}, "description": "A viral infection that affects the liver.", "treatment": "Antiviral medications."},
    "Tuberculosis (TB)": {"symptoms": {"Persistent Cough (sometimes with blood)": 1, "Weight Loss": 1, "Night Sweats": 1, "Fever": 1}, "description": "A bacterial infection that usually affects the lungs.", "treatment": "Antibiotics for a prolonged period."},
    "Mononucleosis (Mono)": {"symptoms": {"Extreme Fatigue": 1, "Sore Throat": 1, "Swollen Lymph Nodes": 1, "Fever": 1}, "description": "A viral infection often caused by the Epstein-Barr virus.", "treatment": "Rest, fluids, pain relievers."},
    "Anxiety Disorder": {"symptoms": {"Excessive Worrying": 1, "Restlessness": 1, "Fatigue": 1, "Difficulty Concentrating": 1}, "description": "A mental health condition characterized by persistent and excessive worry.", "treatment": "Therapy, medication, lifestyle changes."},
    "Depression": {"symptoms": {"Persistent Sadness": 1, "Loss of Interest": 1, "Fatigue": 1, "Changes in Appetite or Sleep": 1}, "description": "A common and serious mood disorder.", "treatment": "Therapy, medication, lifestyle changes."},
    "Panic Disorder": {"symptoms": {"Sudden Feelings of Terror": 1, "Rapid Heartbeat": 1, "Shortness of Breath": 1, "Dizziness": 1}, "description": "An anxiety disorder characterized by recurrent, unexpected panic attacks.", "treatment": "Therapy, medication."},
    "Obsessive-Compulsive Disorder (OCD)": {"symptoms": {"Recurrent, Intrusive Thoughts (Obsessions)": 1, "Repetitive Behaviors (Compulsions)": 1}, "description": "A mental health disorder characterized by obsessions and compulsions.", "treatment": "Therapy, medication."},
    "Post-Traumatic Stress Disorder (PTSD)": {"symptoms": {"Flashbacks": 1, "Nightmares": 1, "Avoidance of Trauma-Related Stimuli": 1, "Hypervigilance": 1}, "description": "A mental health condition that can develop after experiencing or witnessing a traumatic event.", "treatment": "Therapy, medication."}

}

def load_environmental_data():
    with open("data/environmental_data.csv", "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

ENVIRONMENTAL_DATA = load_environmental_data()

def adjust_for_environment(disease, confidence, region):
    for data in ENVIRONMENTAL_DATA:
        if data["Region"] == region:
            if disease in data:
                return confidence * float(data[disease + " Risk"])
    return confidence

@main.route('/')
def index():
    return render_template('index.html', symptoms=SYMPTOMS)

@main.route('/diagnose', methods=['POST'])
def diagnose():
    responses = request.form.to_dict()
    region = request.form.get("region", "default")
    matched_disease = None
    explanation = None

    for disease, data in DISEASES.items():
        total_weight = sum(data["symptoms"].values())
        matched_weight = sum(data["symptoms"][symptom] for symptom in data["symptoms"] if responses.get(symptom) == "yes")
        confidence = (matched_weight / total_weight) * 100
        confidence = adjust_for_environment(disease, confidence, region)

        if matched_weight > 0 and (not matched_disease or confidence > matched_disease["confidence"]):
            matched_disease = {
                "name": disease,
                "description": data["description"],
                "treatment": data["treatment"],
                "confidence": confidence,
                "matched_symptoms": [symptom for symptom in data["symptoms"] if responses.get(symptom) == "yes"]
            }

    if matched_disease:
        explanation = f"{matched_disease['name']} (matched {len(matched_disease['matched_symptoms'])}/{len(data['symptoms'])} key symptoms: {', '.join(matched_disease['matched_symptoms'])})"
        return render_template(
            'index.html',
            symptoms=SYMPTOMS,
            diagnosis=matched_disease["name"],
            description=matched_disease["description"],
            treatment=matched_disease["treatment"],
            explanation=explanation
        )
    else:
        return render_template(
            'index.html',
            symptoms=SYMPTOMS,
            diagnosis="No specific diagnosis found",
            description="We could not match your symptoms to a known disease.",
            treatment="Please consult a healthcare professional for further assistance."
        )

@main.route('/feedback', methods=['POST'])
def feedback():
    diagnosis = request.form["diagnosis"]
    feedback = request.form["feedback"]
    # Store feedback in a database or file
    with open("feedback.csv", "a") as f:
        f.write(f"{diagnosis},{feedback}\n")
    return "Thank you for your feedback!"