import subprocess
import sys
import random
import json
import os
import re

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package {package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

# Load JSON files
def load_json_file(file_name):
    file_path = os.path.join(os.path.dirname(__file__), "data", file_name)
    with open(file_path, "r") as file:
        data = json.load(file)
    
    # Ensure data is a list (if your JSON structure is a list)
    if isinstance(data, list):
        # Remove duplicates by converting to a set and back to a list
        data = list({json.dumps(item, sort_keys=True) for item in data})
        data = [json.loads(item) for item in data]
    
    return data

ARTFORM = load_json_file("artform.json")
PHOTO_TYPE = load_json_file("photo_type.json")
BODY_TYPES = load_json_file("body_types.json")
DEFAULT_TAGS = load_json_file("default_tags.json")
ROLES = load_json_file("roles.json")
HAIRSTYLES = load_json_file("hairstyles.json")
ADDITIONAL_DETAILS = load_json_file("additional_details.json")
PHOTOGRAPHY_STYLES = load_json_file("photography_styles.json")
DEVICE = load_json_file("device.json")
PHOTOGRAPHER = load_json_file("photographer.json")
ARTIST = load_json_file("artist.json")
DIGITAL_ARTFORM = load_json_file("digital_artform.json")
PLACE = load_json_file("place.json")
LIGHTING = load_json_file("lighting.json")
CLOTHING = load_json_file("clothing.json")
COMPOSITION = load_json_file("composition.json")
POSE = load_json_file("pose.json")
BACKGROUND = load_json_file("background.json")
FACE_FEATURES = load_json_file("face_features.json")
EYE_COLORS = load_json_file("eye_colors.json")
FACIAL_HAIR = load_json_file("facial_hair.json")
SKIN_TONE = load_json_file("skin_tone.json")
AGE_GROUP = load_json_file("age_group.json")
ETHNICITY = load_json_file("ethnicity.json")
ACCESSORIES = load_json_file("accessories.json")
EXPRESSION = load_json_file("expression.json")
TATTOOS_SCARS = load_json_file("tattoos_scars.json")
MAKEUP_STYLES = load_json_file("makeup_styles.json")
HAIR_COLOR = load_json_file("hair_color.json")
BODY_MARKINGS = load_json_file("body_markings.json")

class PromptGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def split_and_choose(self, input_str):
        choices = [choice.strip() for choice in input_str.split(",")]
        return self.rng.choices(choices, k=1)[0]

    def get_choice(self, input_str, default_choices):
        if input_str.lower() == "disabled":
            return ""
        elif "," in input_str:
            return self.split_and_choose(input_str)
        elif input_str.lower() == "random":
            return self.rng.choices(default_choices, k=1)[0]
        else:
            return input_str

    def clean_consecutive_commas(self, input_string):
        cleaned_string = re.sub(r',\s*,', ',', input_string)
        return cleaned_string

    def process_string(self, replaced, seed):
        replaced = re.sub(r'\s*,\s*', ',', replaced)
        replaced = re.sub(r',+', ',', replaced)
        original = replaced
        
        first_break_clipl_index = replaced.find("BREAK_CLIPL")
        second_break_clipl_index = replaced.find("BREAK_CLIPL", first_break_clipl_index + len("BREAK_CLIPL"))
        
        if first_break_clipl_index != -1 and second_break_clipl_index != -1:
            clip_content_l = replaced[first_break_clipl_index + len("BREAK_CLIPL"):second_break_clipl_index]
            replaced = replaced[:first_break_clipl_index].strip(", ") + replaced[second_break_clipl_index + len("BREAK_CLIPL"):].strip(", ")
            clip_l = clip_content_l
        else:
            clip_l = ""
        
        first_break_clipg_index = replaced.find("BREAK_CLIPG")
        second_break_clipg_index = replaced.find("BREAK_CLIPG", first_break_clipg_index + len("BREAK_CLIPG"))
        
        if first_break_clipg_index != -1 and second_break_clipg_index != -1:
            clip_content_g = replaced[first_break_clipg_index + len("BREAK_CLIPG"):second_break_clipg_index]
            replaced = replaced[:first_break_clipg_index].strip(", ") + replaced[second_break_clipg_index + len("BREAK_CLIPG"):].strip(", ")
            clip_g = clip_content_g
        else:
            clip_g = ""
        
        t5xxl = replaced
        
        original = original.replace("BREAK_CLIPL", "").replace("BREAK_CLIPG", "")
        original = re.sub(r'\s*,\s*', ',', original)
        original = re.sub(r',+', ',', original)
        clip_l = re.sub(r'\s*,\s*', ',', clip_l)
        clip_l = re.sub(r',+', ',', clip_l)
        clip_g = re.sub(r'\s*,\s*', ',', clip_g)
        clip_g = re.sub(r',+', ',', clip_g)
        if clip_l.startswith(","):
            clip_l = clip_l[1:]
        if clip_g.startswith(","):
            clip_g = clip_g[1:]
        if original.startswith(","):
            original = original[1:]
        if t5xxl.startswith(","):
            t5xxl = t5xxl[1:]

        return original, seed, t5xxl, clip_l, clip_g


    def generate_prompt(self, seed, custom, subject, artform, photo_type, body_types, default_tags, roles, hairstyles,
                        additional_details, photography_styles, device, photographer, artist, digital_artform,
                        place, lighting, clothing, composition, pose, background, face_features, eye_colors, facial_hair, 
                        skin_tone, age_group, ethnicity, accessories, expression, tattoos_scars, makeup_styles,
                        hair_color, body_markings, *args):
        kwargs = locals()
        del kwargs['self']

        seed = kwargs.get("seed", 0)
        if seed is not None:
            self.rng = random.Random(seed)
        components = []
        custom = kwargs.get("custom", "")
        if custom:
            components.append(custom)
        is_photographer = kwargs.get("artform", "").lower() == "photography" or (
            kwargs.get("artform", "").lower() == "random"
            and self.rng.choice([True, False])
        )

        subject = kwargs.get("subject", "")

        if is_photographer:
            selected_photo_style = self.get_choice(kwargs.get("photography_styles", ""), PHOTOGRAPHY_STYLES)
            if not selected_photo_style:
                selected_photo_style = "photography"
            components.append(selected_photo_style)
            if kwargs.get("photography_style", "") != "disabled" and kwargs.get("default_tags", "") != "disabled" or subject != "":
                components.append(" of")
        
        default_tags = kwargs.get("default_tags", "random")
        body_type = kwargs.get("body_types", "")
        if not subject:
            if default_tags == "random":
                if body_type != "disabled" and body_type != "random":
                    selected_subject = self.get_choice(kwargs.get("default_tags", ""), DEFAULT_TAGS).replace("a ", "").replace("an ", "")
                    components.append("a ")
                    components.append(body_type)
                    components.append(selected_subject)
                elif body_type == "disabled":
                    selected_subject = self.get_choice(kwargs.get("default_tags", ""), DEFAULT_TAGS)
                    components.append(selected_subject)
                else:
                    body_type = self.get_choice(body_type, BODY_TYPES)
                    components.append("a ")
                    components.append(body_type)
                    selected_subject = self.get_choice(kwargs.get("default_tags", ""), DEFAULT_TAGS).replace("a ", "").replace("an ", "")
                    components.append(selected_subject)
            elif default_tags == "disabled":
                pass
            else:
                components.append(default_tags)
        else:
            if body_type != "disabled" and body_type != "random":
                components.append("a ")
                components.append(body_type)
            elif body_type == "disabled":
                pass
            else:
                body_type = self.get_choice(body_type, BODY_TYPES)
                components.append("a ")
                components.append(body_type)
            components.append(subject)

        params = [
            ("roles", ROLES),
            ("hairstyles", HAIRSTYLES),
            ("clothing", ADDITIONAL_DETAILS),
        ]
        for param in params:
            components.append(self.get_choice(kwargs.get(param[0], ""), param[1]))
        for i in reversed(range(len(components))):
            if components[i] in PLACE:
                components[i] += ","
                break
        if kwargs.get("clothing", "") != "disabled" and kwargs.get("clothing", "") != "random":
            components.append(", dressed in ")
            clothing = kwargs.get("clothing", "")
            components.append(clothing)
        elif kwargs.get("clothing", "") == "random":
            components.append(", dressed in ")
            clothing = self.get_choice(kwargs.get("clothing", ""), CLOTHING)
            components.append(clothing)

        if kwargs.get("composition", "") != "disabled" and kwargs.get("composition", "") != "random":
            components.append(",")
            composition = kwargs.get("composition", "")
            components.append(composition)
        elif kwargs.get("composition", "") == "random": 
            components.append(",")
            composition = self.get_choice(kwargs.get("composition", ""), COMPOSITION)
            components.append(composition)
        
        if kwargs.get("pose", "") != "disabled" and kwargs.get("pose", "") != "random":
            components.append(",")
            pose = kwargs.get("pose", "")
            components.append(pose)
        elif kwargs.get("pose", "") == "random":
            components.append(",")
            pose = self.get_choice(kwargs.get("pose", ""), POSE)
            components.append(pose)
        components.append("BREAK_CLIPG")
        if kwargs.get("background", "") != "disabled" and kwargs.get("background", "") != "random":
            components.append(",")
            background = kwargs.get("background", "")
            components.append(background)
        elif kwargs.get("background", "") == "random": 
            components.append(",")
            background = self.get_choice(kwargs.get("background", ""), BACKGROUND)
            components.append(background)

        if kwargs.get("place", "") != "disabled" and kwargs.get("place", "") != "random":
            components.append(",")
            place = kwargs.get("place", "")
            components.append(place)
        elif kwargs.get("place", "") == "random": 
            components.append(",")
            place = self.get_choice(kwargs.get("place", ""), PLACE)
            components.append(place + ",")

        lighting = kwargs.get("lighting", "").lower()
        if lighting == "random":
            selected_lighting = ", ".join(self.rng.sample(LIGHTING, self.rng.randint(2, 5)))
            components.append(",")
            components.append(selected_lighting)
        elif lighting == "disabled":
            pass
        else:
            components.append(", ")
            components.append(lighting)

        # Add new parameters after lighting
        components.append("BREAK_CLIPG")
        params = [
            ("face_features", FACE_FEATURES),
            ("eye_colors", EYE_COLORS),
            ("skin_tone", SKIN_TONE),
            ("age_group", AGE_GROUP),
            ("ethnicity", ETHNICITY),
            ("accessories", ACCESSORIES),
            ("expression", EXPRESSION),
            ("tattoos_scars", TATTOOS_SCARS),
            ("hair_color", HAIR_COLOR),
            ("body_markings", BODY_MARKINGS),
        ]
        for param in params:
            components.append(self.get_choice(kwargs.get(param[0], ""), param[1]))

        # Conditional logic for facial_hair and makeup_styles
        if "man" in kwargs.get("default_tags", "").lower():
            components.append(self.get_choice(kwargs.get("facial_hair", ""), FACIAL_HAIR))
        if "woman" in kwargs.get("default_tags", "").lower():
            components.append(self.get_choice(kwargs.get("makeup_styles", ""), MAKEUP_STYLES))

        components.append("BREAK_CLIPL")
        if is_photographer:
            if kwargs.get("photo_type", "") != "disabled":
                photo_type_choice = self.get_choice(kwargs.get("photo_type", ""), PHOTO_TYPE)
                if photo_type_choice and photo_type_choice != "random" and photo_type_choice != "disabled":
                    random_value = round(self.rng.uniform(1.1, 1.5), 1)
                    components.append(f", ({photo_type_choice}:{random_value}), ")

            params = [
                ("device", DEVICE),
                ("photographer", PHOTOGRAPHER),
            ]
            components.extend([self.get_choice(kwargs.get(param[0], ""), param[1]) for param in params])
            if kwargs.get("device", "") != "disabled":
                components[-2] = f", shot on {components[-2]}"
            if kwargs.get("photographer", "") != "disabled":
                components[-1] = f", photo by {components[-1]}"
        else:
            digital_artform_choice = self.get_choice(kwargs.get("digital_artform", ""), DIGITAL_ARTFORM)
            if digital_artform_choice:
                components.append(f"{digital_artform_choice}")
            if kwargs.get("artist", "") != "disabled":
                components.append(f"by {self.get_choice(kwargs.get('artist', ''), ARTIST)}")
        components.append("BREAK_CLIPL")

        prompt = " ".join(components)
        prompt = re.sub(" +", " ", prompt)
        replaced = prompt.replace("of as", "of")
        replaced = self.clean_consecutive_commas(replaced)

        return self.process_string(replaced, seed)


class FluxPromptGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": random.randint(0, 30000), "min": 0, "max": 30000, "step": 1}),
                "custom": ("STRING", {"multiline": True, "default": ""}),
                "subject": ("STRING", {"multiline": True, "default": ""}),
                "artform": (["disabled", "random"] + ARTFORM, {"default": "disabled"}),
                "photo_type": (["disabled", "random"] + PHOTO_TYPE, {"default": "disabled"}),
                "body_types": (["disabled", "random"] + BODY_TYPES, {"default": "disabled"}),
                "default_tags": (["disabled", "random"] + DEFAULT_TAGS, {"default": "disabled"}),
                "roles": (["disabled", "random"] + ROLES, {"default": "disabled"}),
                "hairstyles": (["disabled", "random"] + HAIRSTYLES, {"default": "disabled"}),
                "additional_details": (["disabled", "random"] + ADDITIONAL_DETAILS, {"default": "disabled"}),
                "photography_styles": (["disabled", "random"] + PHOTOGRAPHY_STYLES, {"default": "disabled"}),
                "device": (["disabled", "random"] + DEVICE, {"default": "disabled"}),
                "photographer": (["disabled", "random"] + PHOTOGRAPHER, {"default": "disabled"}),
                "artist": (["disabled", "random"] + ARTIST, {"default": "disabled"}),
                "digital_artform": (["disabled", "random"] + DIGITAL_ARTFORM, {"default": "disabled"}),
                "place": (["disabled", "random"] + PLACE, {"default": "disabled"}),
                "lighting": (["disabled", "random"] + LIGHTING, {"default": "disabled"}),
                "clothing": (["disabled", "random"] + CLOTHING, {"default": "disabled"}),
                "composition": (["disabled", "random"] + COMPOSITION, {"default": "disabled"}),
                "pose": (["disabled", "random"] + POSE, {"default": "disabled"}),
                "background": (["disabled", "random"] + BACKGROUND, {"default": "disabled"}),
                "face_features": (["disabled", "random"] + FACE_FEATURES, {"default": "disabled"}),
                "eye_colors": (["disabled", "random"] + EYE_COLORS, {"default": "disabled"}),
                "facial_hair": (["disabled", "random"] + FACIAL_HAIR, {"default": "disabled"}),
                "skin_tone": (["disabled", "random"] + SKIN_TONE, {"default": "disabled"}),
                "age_group": (["disabled", "random"] + AGE_GROUP, {"default": "disabled"}),
                "ethnicity": (["disabled", "random"] + ETHNICITY, {"default": "disabled"}),
                "accessories": (["disabled", "random"] + ACCESSORIES, {"default": "disabled"}),
                "expression": (["disabled", "random"] + EXPRESSION, {"default": "disabled"}),
                "tattoos_scars": (["disabled", "random"] + TATTOOS_SCARS, {"default": "disabled"}),
                "makeup_styles": (["disabled", "random"] + MAKEUP_STYLES, {"default": "disabled"}),
                "hair_color": (["disabled", "random"] + HAIR_COLOR, {"default": "disabled"}),
                "body_markings": (["disabled", "random"] + BODY_MARKINGS, {"default": "disabled"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "Prompt"

    def execute(self, seed, custom, subject, artform, photo_type, body_types, default_tags, roles, hairstyles, additional_details, photography_styles, device, photographer, artist, digital_artform, place, lighting, clothing, composition, pose, background, face_features, eye_colors, facial_hair, skin_tone, age_group, ethnicity, accessories, expression, tattoos_scars, makeup_styles, hair_color, body_markings):
        prompt_generator = PromptGenerator(seed)
        prompt, seed, t5xxl_output, clip_l_output, clip_g_output = prompt_generator.generate_prompt(
            seed, custom, subject, artform, photo_type, body_types, default_tags, roles, hairstyles, additional_details,
            photography_styles, device, photographer, artist, digital_artform, place, lighting, clothing, composition,
            pose, background, face_features, eye_colors, facial_hair, skin_tone, age_group, ethnicity, accessories, 
            expression, tattoos_scars, makeup_styles, hair_color, body_markings
        )
        return (prompt, seed, t5xxl_output, clip_l_output, clip_g_output)

    @classmethod
    def IS_CHANGED(cls, *args):
        return True

# Node export details
NODE_CLASS_MAPPINGS = {
    "FluxPromptGenerator": FluxPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPromptGenerator": "Flux Prompt Generator"
}