# **Flux-Prompt-Generator**

**Flux Prompt Generator** is a **ComfyUI** node that provides a flexible and customizable prompt generator for generating detailed and creative prompts for image generation models.
based on the work by [Aitrepreneur](https://huggingface.co/Aitrepreneur) found here [Flux Prompt Generator python code](https://huggingface.co/Aitrepreneur/FLUX-Prompt-Generator/blob/main/app.py) and modified to work with ComfyUI by [FairyRoot](https://github.com/fairy-root)

![Flux Prompt Generator](https://i.imgur.com/I3nQzaa.png "Displaying workflow")

## Overview

The **Flux Prompt Generator** utilizes a collection of JSON data files containing various categories of descriptive terms. These categories include:

- **Artform:** Photography, Digital Art, etc.
- **Photo Type:** Portrait, Landscape, etc.
- **Body Types:** Muscular, Thin, etc.
- **Default Tags:** Man, Woman, Child, etc.
- **Roles:** Knight, Wizard, etc.
- **Hairstyles:** Long, Short, Braided, etc.
- **Additional Details:** Clothing, Accessories, etc.
- **Photography Styles:** Cinematic, Realistic, etc.
- **Device:** Camera models, etc.
- **Photographer:** Famous photographers, etc.
- **Artist:** Famous artists, etc.
- **Digital Artform:** Pixel Art, 3D Render, etc.
- **Place:** Forest, City, etc.
- **Lighting:** Soft, Harsh, etc.
- **Clothing:** Dress, Suit, etc.
- **Composition:** Rule of Thirds, Golden Ratio, etc.
- **Pose:** Standing, Sitting, etc.
- **Background:** Plain, Detailed, etc.
- **Face Features:** Sharp Jawline, High Cheekbones, etc.
- **Eye Colors:** Blue, Green, Brown, etc.
- **Facial Hair:** Beard, Mustache, etc.
- **Skin Tone:** Pale, Dark, etc.
- **Age Group:** Child, Teenager, Adult, etc.
- **Ethnicity:** Various ethnicities and cultural backgrounds.
- **Accessories:** Glasses, Hats, Jewelry, etc.
- **Expression:** Smile, Frown, Surprise, etc.
- **Tattoos & Scars:** Detailed descriptions of body modifications.
- **Makeup Styles:** Natural, Glamorous, etc.
- **Hair Color:** Blonde, Brown, Black, etc.
- **Body Markings:** Birthmarks, Moles, Freckles, etc.

![Flux Prompt Generator](https://i.imgur.com/0TNizfp.png "Displaying node")

The node allows you to select specific terms or choose "random" to let the generator pick random terms from the corresponding JSON file. This randomness adds a degree of unpredictability and creativity to the generated prompts.

## Installation

1. **cd** to the custom_nodes folder inside of **ComfyUI** directory
2. **cmd** in the address bar, then use this command:
```
git clone https://github.com/fairy-root/Flux-Prompt-Generator.git
```

## Usage

1. **Add the "Flux Prompt Generator" node to your ComfyUI workflow.**
2. **Configure the desired parameters:**
    - **Seed:** Controls the randomness of the generator.
    - **Custom:** Add any custom text to the prompt.
    - **Subject:** Specify the main subject of the image.
    - **Artform:** Choose the desired art form (Photography, Digital Art, etc.).
    - **... (All other parameters as described in the Overview section)**

3. **Connect the output of the node to a text-to-image model (like Flux or Stable Diffusion...etc) to generate images based on the generated prompt.**

## Example

Let's say you want to generate a prompt for a portrait photograph of a woman with long hair, wearing a dress, and standing in a forest. You could configure the node with the following parameters:

- **Artform:** Photography
- **Photo Type:** Portrait
- **Default Tags:** Woman
- **Hairstyles:** Long Hair
- **Clothing:** Dress
- **Place:** Forest

The node would then generate a prompt similar to: "photography of a woman with long hair, dressed in a dress, in a forest."

## Donation

Your support is appreciated:

- USDt (TRC20): `TGCVbSSJbwL5nyXqMuKY839LJ5q5ygn2uS`
- BTC: `13GS1ixn2uQAmFQkte6qA5p1MQtMXre6MT`
- ETH (ERC20): `0xdbc7a7dafbb333773a5866ccf7a74da15ee654cc`
- LTC: `Ldb6SDxUMEdYQQfRhSA3zi4dCUtfUdsPou`

## Author and Contact

- GitHub: [FairyRoot](https://github.com/fairy-root)
- Telegram: [@FairyRoot](https://t.me/FairyRoot)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.