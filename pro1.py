import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile

# Define PDF class
class PDF(FPDF):
    def __init__(self, photo_path=None):
        super().__init__()
        self.photo_path = photo_path

    def header(self):
        if self.photo_path:
            self.image(self.photo_path, 10, 8, 33)
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, st.session_state["name"], ln=True, align="R")
        self.set_font("Arial", "", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"{st.session_state['email']} | {st.session_state['phone']}", ln=True, align="R")
        self.cell(0, 10, st.session_state["location"], ln=True, align="R")
        self.cell(0, 10, f"LinkedIn: {st.session_state['linkedin']}", ln=True, align="R")
        self.cell(0, 10, f"GitHub: {st.session_state['github']}", ln=True, align="R")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, content):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, content)
        self.ln(2)


# Streamlit UI
st.title("🎓 BTech Fresher Resume Builder")

with st.form("resume_form"):
    st.subheader("👤 Personal Details")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    location = st.text_input("Location")
    linkedin = st.text_input("LinkedIn Profile URL")
    github = st.text_input("GitHub Profile URL")
    photo = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

    st.subheader("🎓 Education")
    degree = st.text_input("Degree (e.g., BTech in Computer Science)")
    college = st.text_input("College Name")
    graduation_year = st.text_input("Year of Graduation")

    st.subheader("🛠️ Skills")
    skills = st.text_area("Skills (comma-separated)")

    st.subheader("💼 Projects")
    projects = st.text_area("List your Academic or Personal Projects")

    st.subheader("📚 Certifications")
    certifications = st.text_area("Relevant Certifications")

    st.subheader("🏆 Achievements")
    achievements = st.text_area("Competitions, Awards, Hackathons etc.")

    st.subheader("🧑‍💼 Internships / Training")
    internships = st.text_area("Internships or Industrial Trainings")

    st.subheader("🌐 Languages Known")
    languages = st.text_input("Languages (e.g., English, Hindi)")

    st.subheader("🎯 Hobbies / Interests")
    hobbies = st.text_input("Sports, Music, Tech Blogs etc.")

    st.subheader("📌 Position Applied For")
    position = st.text_input("Job Role")

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    # Save inputs in session state
    st.session_state.update({
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "github": github,
    })

    photo_path = None
    if photo:
        img = Image.open(photo)
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_img.name)
        photo_path = temp_img.name

    # Generate PDF
    pdf = PDF(photo_path=photo_path)
    pdf.add_page()

    pdf.section_title("Career Objective")
    pdf.section_body(
        f"Recent BTech graduate in {degree} from {college}, passionate about technology and innovation. "
        f"Aspiring to work as a {position} where I can contribute my problem-solving skills, engineering knowledge, and passion for learning."
    )

    pdf.section_title("Education")
    pdf.section_body(f"{degree} from {college} ({graduation_year})")

    pdf.section_title("Skills")
    pdf.section_body(skills)

    pdf.section_title("Projects")
    pdf.section_body(projects)

    pdf.section_title("Certifications")
    pdf.section_body(certifications)

    pdf.section_title("Achievements")
    pdf.section_body(achievements)

    pdf.section_title("Internships / Training")
    pdf.section_body(internships)

    pdf.section_title("Languages Known")
    pdf.section_body(languages)

    pdf.section_title("Hobbies / Interests")
    pdf.section_body(hobbies)

    # Export
    pdf_output = pdf.output(dest="S").encode("latin1")
    st.download_button("📄 Download Resume PDF", data=pdf_output, file_name=f"{name}_Resume.pdf", mime="application/pdf")
