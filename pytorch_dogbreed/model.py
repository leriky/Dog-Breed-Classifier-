import torch
from torchvision import transforms
from PIL import Image

def get_tensor(image):
    transform = transforms.Compose([
        transforms.Resize(size=256),#resizes the image to 256X256
        transforms.CenterCrop(size=224),# cropped the images 224X224 at the center
        transforms.ToTensor()#converts the image pixel range from 0-255 to 0-1 by dividing each pixel by 255
    ])
    test_image = Image.open(image)
    test_image_tensor = transform(test_image)
    return test_image_tensor.unsqueeze(0)

idx_to_breed = {
    0: 'Affenpinscher',
    1: 'Afghan_hound',
    2: 'Airedale_terrier',
    3: 'Akita',
    4: 'Alaskan_malamute',
    5: 'American_eskimo_dog',
    6: 'American_foxhound',
    7: 'American_staffordshire_terrier',
    8: 'American_water_spaniel',
    9: 'Anatolian_shepherd_dog',
    10: 'Australian_cattle_dog',
    11: 'Australian_shepherd',
    12: 'Australian_terrier',
    13: 'Basenji',
    14: 'Basset_hound',
    15: 'Beagle',
    16: 'Bearded_collie',
    17: 'Beauceron',
    18: 'Bedlington_terrier',
    19: 'Belgian_malinois',
    20: 'Belgian_sheepdog',
    21: 'Belgian_tervuren',
    22: 'Bernese_mountain_dog',
    23: 'Bichon_frise',
    24: 'Black_and_tan_coonhound',
    25: 'Black_russian_terrier',
    26: 'Bloodhound',
    27: 'Bluetick_coonhound',
    28: 'Border_collie',
    29: 'Border_terrier',
    30: 'Borzoi',
    31: 'Boston_terrier',
    32: 'Bouvier_des_flandres',
    33: 'Boxer',
    34: 'Boykin_spaniel',
    35: 'Briard',
    36: 'Brittany',
    37: 'Brussels_griffon',
    38: 'Bull_terrier',
    39: 'Bulldog',
    40: 'Bullmastiff',
    41: 'Cairn_terrier',
    42: 'Canaan_dog',
    43: 'Cane_corso',
    44: 'Cardigan_welsh_corgi',
    45: 'Cavalier_king_charles_spaniel',
    46: 'Chesapeake_bay_retriever',
    47: 'Chihuahua',
    48: 'Chinese_crested',
    49: 'Chinese_shar-pei',
    50: 'Chow_chow',
    51: 'Clumber_spaniel',
    52: 'Cocker_spaniel',
    53: 'Collie',
    54: 'Curly-coated_retriever',
    55: 'Dachshund',
    56: 'Dalmatian',
    57: 'Dandie_dinmont_terrier',
    58: 'Doberman_pinscher',
    59: 'Dogue_de_bordeaux',
    60: 'English_cocker_spaniel',
    61: 'English_setter',
    62: 'English_springer_spaniel',
    63: 'English_toy_spaniel',
    64: 'Entlebucher_mountain_dog',
    65: 'Field_spaniel',
    66: 'Finnish_spitz',
    67: 'Flat-coated_retriever',
    68: 'French_bulldog',
    69: 'German_pinscher',
    70: 'German_shepherd_dog',
    71: 'German_shorthaired_pointer',
    72: 'German_wirehaired_pointer',
    73: 'Giant_schnauzer',
    74: 'Glen_of_imaal_terrier',
    75: 'Golden_retriever',
    76: 'Gordon_setter',
    77: 'Great_dane',
    78: 'Great_pyrenees',
    79: 'Greater_swiss_mountain_dog',
    80: 'Greyhound',
    81: 'Havanese',
    82: 'Ibizan_hound',
    83: 'Icelandic_sheepdog',
    84: 'Irish_red_and_white_setter',
    85: 'Irish_setter',
    86: 'Irish_terrier',
    87: 'Irish_water_spaniel',
    88: 'Irish_wolfhound',
    89: 'Italian_greyhound',
    90: 'Japanese_chin',
    91: 'Keeshond',
    92: 'Kerry_blue_terrier',
    93: 'Komondor',
    94: 'Kuvasz',
    95: 'Labrador_retriever',
    96: 'Lakeland_terrier',
    97: 'Leonberger',
    98: 'Lhasa_apso',
    99: 'Lowchen',
    100: 'Maltese',
    101: 'Manchester_terrier',
    102: 'Mastiff',
    103: 'Miniature_schnauzer',
    104: 'Neapolitan_mastiff',
    105: 'Newfoundland',
    106: 'Norfolk_terrier',
    107: 'Norwegian_buhund',
    108: 'Norwegian_elkhound',
    109: 'Norwegian_lundehund',
    110: 'Norwich_terrier',
    111: 'Nova_scotia_duck_tolling_retriever',
    112: 'Old_english_sheepdog',
    113: 'Otterhound',
    114: 'Papillon',
    115: 'Parson_russell_terrier',
    116: 'Pekingese',
    117: 'Pembroke_welsh_corgi',
    118: 'Petit_basset_griffon_vendeen',
    119: 'Pharaoh_hound',
    120: 'Plott',
    121: 'Pointer',
    122: 'Pomeranian',
    123: 'Poodle',
    124: 'Portuguese_water_dog',
    125: 'Saint_bernard',
    126: 'Silky_terrier',
    127: 'Smooth_fox_terrier',
    128: 'Tibetan_mastiff',
    129: 'Welsh_springer_spaniel',
    130: 'Wirehaired_pointing_griffon',
    131: 'Xoloitzcuintli',
    132: 'Yorkshire_terrier'
    }

def get_model():
    model = torch.load("./resnet50_final", map_location=torch.device('cpu'))
    model.eval()
    return model

model = get_model()

def prediction(model, image):    
    test_image_tensor = get_tensor(image)
    with torch.no_grad():
        model.eval()
        # Model outputs log probabilities
        out = model(test_image_tensor)
        prediction_prob = torch.exp(out)
        top5_prob, top5_idx = torch.topk(prediction_prob, 5)
        top5_prob, top5_idx =  top5_prob.cpu().numpy()[0], top5_idx.cpu().numpy()[0]
        top5_breed = []
        for idx, prob in zip(top5_idx, top5_prob):
            print("Breed :  ", idx_to_breed[idx], "   Predcition : ", prob)
            top5_breed.append(idx_to_breed[idx])
        return top5_prob, top5_breed