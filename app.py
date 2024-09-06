import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Function to plot BMI categories
def plot_bmi_chart():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create weight and height ranges
    height_range = np.linspace(1.0, 2.5, 500)
    weight_range = np.linspace(30, 150, 500)
    height_grid, weight_grid = np.meshgrid(height_range, weight_range)
    bmi_grid = weight_grid / (height_grid ** 2)

    # Plot BMI categories
    contour = ax.contourf(height_grid, weight_grid, bmi_grid, levels=[0, 18.5, 24.9, 29.9, 40], colors=['#FFDDDD', '#FFFFDD', '#FFFF99', '#FF9999'], alpha=0.6)
    ax.contour(height_grid, weight_grid, bmi_grid, levels=[18.5, 24.9, 29.9], colors=['blue', 'green', 'red'], linestyles='dashed')
    
    # Labels and title
    ax.set_xlabel('Height (m)')
    ax.set_ylabel('Weight (kg)')
    ax.set_title('BMI Categories by Height and Weight')
    ax.legend(['Underweight', 'Normal weight', 'Overweight', 'Obesity'], loc='upper right')

    # Display the plot in Streamlit
    st.pyplot(fig)

# Function to get avatar image path based on BMI
def get_avatar_image_path(bmi):
    if bmi < 18.5:
        return "images/underweight.jpg"
    elif 18.5 <= bmi < 24.9:
        return "images/normal_weight.jpg"
    elif 25 <= bmi < 29.9:
        return "images/overweight.jpg"
    else:
        return "images/obesity.jpg"

# Set up navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Introduction", "BMI Analyzer"])

# Introduction Page
if page == "Introduction":
    st.title("Introduction to BMI")
    st.write(
        """
        **Body Mass Index (BMI)** is a measure of body fat based on height and weight. 
        It is used to categorize individuals into different weight categories such as 
        underweight, normal weight, overweight, and obesity. 

        The BMI formula is:
        \[
        \text{BMI} = \frac{\text{weight (kg)}}{\text{height (m)}^2}
        \]

        - **Underweight:** BMI < 18.5
        - **Normal weight:** 18.5 ≤ BMI < 24.9
        - **Overweight:** 25 ≤ BMI < 29.9
        - **Obesity:** BMI ≥ 30

        Understanding your BMI can help you make informed decisions about your health and 
        guide you in setting fitness goals.
        """
    )

    # Plot BMI chart
    st.write("BMI Categories Chart")
    plot_bmi_chart()

# BMI Analyzer Page
elif page == "BMI Analyzer":
    st.title("BMI Analyzer")
    st.write("Calculate your Body Mass Index (BMI) and get personalized health suggestions.")

    # User input for weight and height using sliders
    weight = st.slider("Select your weight (kg)", min_value=0.0, max_value=200.0, value=70.0, step=0.1)
    height = st.slider("Select your height (m)", min_value=0.0, max_value=2.5, value=1.75, step=0.01)

    if st.button("Calculate BMI"):
        if height > 0:
            bmi = weight / (height ** 2)
            st.write(f"Your BMI is {bmi:.2f}")

            # Health feedback based on BMI value
            if bmi < 18.5:
                st.warning("Underweight")
                st.write(
                    """
                    **Suggestions to Improve Your Health:**
                    - Increase your caloric intake with nutrient-rich foods.
                    - Include more protein and healthy fats in your diet.
                    - Consider consulting a healthcare provider or dietitian for personalized advice.
                    - Engage in regular exercise to build muscle mass.
                    """
                )
            elif 18.5 <= bmi < 24.9:
                st.success("Normal weight")
                st.write(
                    """
                    **Suggestions to Maintain Your Health:**
                    - Continue eating a balanced diet with a mix of proteins, carbohydrates, and fats.
                    - Maintain regular physical activity to stay fit.
                    - Monitor your weight regularly to ensure it remains stable.
                    - Stay hydrated and get adequate sleep.
                    """
                )
            elif 25 <= bmi < 29.9:
                st.warning("Overweight")
                st.write(
                    """
                    **Suggestions to Improve Your Health:**
                    - Aim for a balanced diet with reduced calorie intake.
                    - Increase physical activity and incorporate both cardio and strength training exercises.
                    - Monitor portion sizes and avoid sugary and high-fat foods.
                    - Consider consulting a healthcare provider for personalized weight management strategies.
                    """
                )
            else:
                st.error("Obesity")
                st.write(
                    """
                    **Suggestions to Improve Your Health:**
                    - Seek professional advice from a healthcare provider for a tailored weight loss plan.
                    - Focus on a balanced, calorie-controlled diet.
                    - Increase physical activity and establish a regular exercise routine.
                    - Consider support from a nutritionist or a weight management program.
                    """
                )

            # Resize and display the avatar image
            avatar_image_path = get_avatar_image_path(bmi)
            with Image.open(avatar_image_path) as img:
                # Resize image while maintaining quality
                base_width = 150  # New width for the resized image
                w_percent = (base_width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((base_width, h_size), Image.LANCZOS)
                st.image(img, caption="Your body shape representation", use_column_width=True)
        else:
            st.error("Height must be greater than zero.")
