def analyze_symptoms(
    symptoms: str
):

    symptoms_lower = symptoms.lower()


    # =========================
    # EMERGENCY CONDITIONS
    # =========================

    if (
        "chest pain" in symptoms_lower
        or
        "difficulty breathing" in symptoms_lower
    ):

        return {

            "risk_level": "HIGH",

            "recommendation":
            "Seek emergency medical attention immediately.",

            "ai_response":
            "Possible cardiovascular or respiratory emergency detected."
        }


    # =========================
    # FEVER
    # =========================

    elif "fever" in symptoms_lower:

        return {

            "risk_level": "MEDIUM",

            "recommendation":
            "Visit a hospital for proper medical evaluation.",

            "ai_response":
            "Possible infection or inflammatory condition detected."
        }


    # =========================
    # HEADACHE
    # =========================

    elif "headache" in symptoms_lower:

        return {

            "risk_level": "LOW",

            "recommendation":
            "Rest, hydrate, and monitor symptoms.",

            "ai_response":
            "Possible stress-related or mild neurological condition."
        }


    # =========================
    # DEFAULT
    # =========================

    return {

        "risk_level": "LOW",

        "recommendation":
        "Consult a healthcare professional if symptoms persist.",

        "ai_response":
        "Symptoms require professional medical evaluation."
    }