import os
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AI Fridge Chef",
    page_icon="🍳",
    layout="centered"
)

# App Header
st.title("🍳 AI Recipe Generator from Fridge Ingredients")
st.markdown("Enter the ingredients you have left in your fridge, and let Gemini Flash cook up a custom recipe for you!")

# Sidebar Configuration for API Key
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input(
    "Enter Gemini API Key", 
    type="password", 
    help="Get your free key from Google AI Studio."
)

# Determine API key source (Streamlit secrets or Sidebar input)
api_key = api_key_input or st.secrets.get("GEMINI_API_KEY", None)

# Main Form Input
ingredients = st.text_area(
    "What's in your fridge?", 
    placeholder="e.g., chicken breast, garlic, soy sauce, broccoli, rice",
    height=100
)

dietary_pref = st.selectbox(
    "Dietary Restrictions / Preferences (Optional)",
    ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Dairy-Free"]
)

# Generate Recipe Action
if st.button("Generate Recipe 🚀", type="primary"):
    # Guard clause: Check for missing API key
    if not api_key:
        st.error("⚠️ Error: Gemini API key is missing. Please enter it in the sidebar or configure it in Streamlit secrets.")
    # Guard clause: Check for empty input
    elif not ingredients.strip():
        st.warning("⚠️ Please enter at least one ingredient found in your fridge.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Using Gemini 1.5 Flash
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Construct Prompt
            prompt = f"""
            You are an expert chef and culinary assistant. 
            The user has the following ingredients available: {ingredients}.
            Dietary restriction/preference: {dietary_pref}.
            
            Please create a creative, delicious meal recipe using these ingredients (you can assume basic pantry staples like salt, pepper, oil, water, and common spices are available).
            
            Format your response clearly with:
            1. **Recipe Title**
            2. **Prep Time & Cook Time**
            3. **Ingredients Needed** (including quantities)
            4. **Step-by-Step Instructions**
            5. **Chef's Tip** for extra flavor
            """
            
            # Call Model with Spinner
            with st.spinner("🍳 Cooking up your recipe with Gemini Flash..."):
                response = model.generate_content(prompt)
                
                # Display Result
                st.success("Here is your custom recipe!")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred while communicating with Gemini: {e}")
