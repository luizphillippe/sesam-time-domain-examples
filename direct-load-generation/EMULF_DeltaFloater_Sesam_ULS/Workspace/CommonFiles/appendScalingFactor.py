import sys
import os

#Edit existing LCOM card to point to new SCAL card
def update_lcom_to_point_to_scaling_factor(file_path):
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('LCOM'):
                new_line = line[:14] +  '1.0   ' + line[20:]
                new_lines.append(new_line)
            else:
                new_lines.append(line)
            new_text = '\n'.join(new_lines)
            with open(file_path, 'w') as f:
                f.write(new_text)
    except Exception as e:
        print(f"Error: {e}")

#Append SCAL card with modified factor 
def append_scaling_factor_to_file(file_path, scaling_factor):
    try:
        with open(file_path, 'a') as file:
            text_to_append = f"SCAL    1.           24.       {scaling_factor}"
            file.write(f"{text_to_append}  \n")
        print(f"Scaling factor {scaling_factor} appended to {file_path} successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"running appendscalingfactor.py in folder {os.getcwd()}")
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <scaling factor>")
        sys.exit(1)

    file_path = sys.argv[1]
    scaling_factor = sys.argv[2]
    update_lcom_to_point_to_scaling_factor(file_path)
    append_scaling_factor_to_file(file_path, scaling_factor)
    