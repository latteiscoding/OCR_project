#!/usr/bin/env python
# coding: utf-8

# In[51]:


# text detect
import pandas as pd
from google.cloud import vision

# pdf to image
import sys
import pathlib
from pdf2image import convert_from_path

# feature allow user to select scan bound
# take full_text_annotation, minX, minY, maxX, maxY
# return text seperate by \n
def text_within(document,x1,y1,x2,y2): 
  text=""
  for page in document.pages:
    for block in page.blocks:
      for paragraph in block.paragraphs:
        for word in paragraph.words:
          for symbol in word.symbols:
            min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
            max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
            if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
              text+=symbol.text
              if(symbol.property.detected_break.type==1 or 
                symbol.property.detected_break.type==3):
                text+=' '
              if(symbol.property.detected_break.type==2):
                text+='\t'
              if(symbol.property.detected_break.type==5):
                text+='\n'
    return text

# call google vision api
# take path to image
# return vision response
# use full_text_annotation here
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
#     print("Texts:")

#     for text in texts:
#         print(f'\n"{text.description}"')
# #         all_result.extend(text.description)
#         vertices = [
#             f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
#         ]

#         print("bounds: {}".format(",".join(vertices)))

#     print(texts[0].description)
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
#     return texts[0].description
    return response;

# convert pdf to response(set dpi 80)
# take in file path return all raw data
def pdf_to_text(path):
    pdf_path = pathlib.Path(path)
    if not pdf_path.is_file():
        sys.exit("Invalid PDF path")
    images = convert_from_path(str(pdf_path.resolve()),dpi = 80)
    all_results = []
    for img in images:
        img.save("temp_image.png", "PNG")
#         img_path = str(pathlib.Path("temp_image.jpg").resolve())
        # Extract text from the temporary image file
        raw_response = detect_text("temp_image.png")
        # Append the results for this page to all_results
        all_results.append(raw_response)
    return all_results

#
def page_format(all_results, bounds = bound):
    dfs = []
    for result in all_results:
        texts = []
        max_row = 0
        for bound in bounds:
            text = text_within(result.full_text_annotation, bound[0], bound[1], bound[2], bound[3])
            list_temp = text.split('\n')
            max_row = max(len(list_temp), max_row)
            texts.append(list_temp)
        for text in texts:
            text.extend([''] * (max_length - len(text)))
        dfs.append(pd.DataFrame(texts).transpose())
    return dfs
        
    


# In[95]:


bounds = [[0, 0, 1300, 10000],[1400, 0, 2000, 10000],[1880, 0, 9999, 10000]]
responses = pdf_to_text("files/sample.pdf")
dfs = page_format(responses, bounds)
df2 = pd.concat(dfs)
output_excel_file = "format_sheet.xlsx"
df2.to_excel(output_excel_file, index=False, header=False)


# In[96]:





# In[99]:


df2


# In[97]:





# In[70]:


test_text = text_within(responses[0].full_text_annotation, 0, 0, 1300, 10000)
test_text.split('\n')


# In[80]:


test_text = text_within(responses[0].full_text_annotation, 1400, 0, 2000, 10000)
test_text.split('\n')


# In[88]:


test_text = text_within(responses[0].full_text_annotation, 1880, 0, 9999, 10000)
test_text.split('\n')


# In[62]:


bounds = [[0, 0, 617, 9999],[590, 0, 770, 9999],[825, 0, 3000, 9999]]
dfs = page_format(responses, bounds)
dfs[0]


# In[55]:


dfs[1]


# In[47]:


t = [1, 2, 3, 5]
t1 = [1, 2,3, 4]
test = pd.DataFrame([t,t1]).transpose()
test


# In[7]:


res = detect_text("files/firstPage.png")


# In[9]:


texts_full = res.full_text_annotation
tests = res.text_annotations


# In[17]:


print(tests)


# In[16]:


print(texts_full)


# In[14]:


def text_within(document,x1,y1,x2,y2): 
  text=""
  for page in document.pages:
    for block in page.blocks:
      for paragraph in block.paragraphs:
        for word in paragraph.words:
          for symbol in word.symbols:
            min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
            max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
            if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
              text+=symbol.text
              if(symbol.property.detected_break.type==1 or 
                symbol.property.detected_break.type==3):
                text+=' '
              if(symbol.property.detected_break.type==2):
                text+='\t'
              if(symbol.property.detected_break.type==5):
                text+='\n'
    return text


# In[18]:


sample_text = text_within(texts_full, 0, 0, 900, 1700)


# In[19]:


print(sample_text)


# In[28]:


sample_text_col2 = text_within(texts_full, 900, 0, 1400, 1700)


# In[29]:


print(sample_text_col2)


# In[24]:


sample_text_col3 = text_within(texts_full, 1370, 0, 3000, 1700)


# In[25]:


print(sample_text_col3)


# In[31]:


list1 = sample_text.split('\n')
list2 = sample_text_col2.split('\n')
list3 = sample_text_col3.split('\n')
max_length = max(len(list1), len(list2), len(list3))
list1.extend([''] * (max_length - len(list1)))
list2.extend([''] * (max_length - len(list2)))
list3.extend([''] * (max_length - len(list3)))

# Create a DataFrame with each list as a column
df = pd.DataFrame({'Column1': list1, 'Column2': list2, 'Column3': list3})


# In[32]:


df


# In[33]:


output_excel_file = "format_sheet.xlsx"
df.to_excel(output_excel_file, index=False, header=False)


# In[ ]:


def get_document_bounds(image_file, feature):
    """Finds the document bounds given an image and feature type.

    Args:
        image_file: path to the image file.
        feature: feature type to detect.

    Returns:
        List of coordinates for the corresponding feature type.
    """
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


# In[ ]:


bounds = get_document_bounds()

