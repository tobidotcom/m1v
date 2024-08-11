import streamlit as st
import subprocess
import os
from tempfile import NamedTemporaryFile

def repair_m1v_file(input_path, output_path):
    """
    Repariert eine .m1v Datei, indem sie in ein abspielbares Format konvertiert wird.
    
    :param input_path: Pfad zur Eingabedatei (.m1v)
    :param output_path: Pfad zur Ausgabedatei (.mp4)
    """
    command = [
        'ffmpeg',
        '-i', input_path,  # Eingabedatei
        '-c:v', 'copy',    # Video-Codec (Kopieren ohne Neukodierung)
        output_path        # Ausgabedatei
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Fehler bei der Konvertierung: {e}")
    except FileNotFoundError:
        st.error("ffmpeg ist nicht installiert oder nicht im PATH verfügbar.")

def main():
    st.title("M1V Video Repair Tool")
    st.write("Lade eine `.m1v`-Datei hoch, um sie zu reparieren und in ein abspielbares Format zu konvertieren.")

    # Datei-Upload
    uploaded_file = st.file_uploader("Wähle eine .m1v Datei", type=["m1v"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)  # Vorschau des hochgeladenen Videos

        # Temporäre Datei für die hochgeladene Datei
        with NamedTemporaryFile(delete=False, suffix=".m1v") as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name

        # Temporäre Datei für die Ausgabedatei
        temp_output_path = temp_input_path.replace(".m1v", "_repariert.mp4")
        
        # Repariere die Datei
        repair_m1v_file(temp_input_path, temp_output_path)

        # Biete die reparierte Datei zum Download an
        if os.path.exists(temp_output_path):
            with open(temp_output_path, "rb") as file:
                btn = st.download_button(
                    label="Repariertes Video herunterladen",
                    data=file,
                    file_name="repariert_video.mp4",
                    mime="video/mp4"
                )

        # Entferne die temporären Dateien
        os.remove(temp_input_path)
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

if __name__ == "__main__":
    main()
