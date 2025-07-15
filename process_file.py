import ocr_recognition


def process_file(csv_file_data, st_lit):
    predicted_name = ocr_recognition.read_image(csv_file_data)
    processed_lines = process_name(predicted_name)
    validity = [determine_validity(processed_lines[i], csv_file_data['CALLER NAME'].tolist()[i]) for i in range(len(processed_lines))]
    print(validity)
    csv_file_data["CALLER NAME THROUGH AI"] = processed_lines
    csv_file_data["MATCH (YES/NO)"] = validity

    return True


def process_name(text_list):
    predicted_name = []
    for i in text_list:
        if len(i) == 0:
            predicted_name.append("No Business Name Presented")
            continue
        elif len(i) == 1:
            predicted_name.append(i[0])
            continue
        text = " ".join(i)
        predicted_name.append(text)
    return predicted_name


def determine_validity(predicted_text, target_text):
    predicted_text = predicted_text.split(" ")
    return any(kw in target_text for kw in predicted_text)
