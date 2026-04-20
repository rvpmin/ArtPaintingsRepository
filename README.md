# ArtPaintingsRepository


This project focuses on building, cleaning, and unifying datasets of artworks from multiple museums, including Mexican museums and the Metropolitan Museum of Art (MET). The goal is to create a structured dataset suitable for analysis and machine learning tasks such as classification.

## Project Overview

The repository contains:

- Data collection from multiple museum sources
- Data cleaning and normalization pipelines
- Integration of heterogeneous datasets into a unified schema
- Feature engineering (dates, dimensions, techniques, materials, etc.)
- Preparation for downstream tasks such as classification and analysis

## Dataset Structure

The final dataset includes the following key columns:

- `title`: Artwork title
- `artist`: Artist name
- `description`: Artwork description
- `image_path`: Local path to the image
- `dimensions`: Raw dimensions text
- `width_cm`, `height_cm`, `depth_cm`: Parsed dimensions
- `artist_nationality`, `artist_birthplace`, `artist_deathplace`
- `artist_sex`
- `type`: Artwork type
- `technique`: Technique
- `support`: Material support (e.g., canvas, paper, wood)
- `theme`, `keywords`
- `country`: Country of origin
- `date`, `year_start`, `year_end`, `estimated`
- `museum`: Source museum

## Data Sources

- Mexican museum collections (MUNAL, Museo Soumaya, MACAY, Museo Frida Kahlo, Museo Arocena, Colección Blaisten)
- Metropolitan Museum of Art (MET) Open Access API

## Data Processing Pipeline

The pipeline includes:

1. **Transformation**
   - Mapping raw fields to a unified schema

2. **Cleaning**
   - Removing inconsistencies
   - Converting empty strings to NaN

3. **Parsing**
   - Dates → `year_start`, `year_end`, `estimated`
   - Dimensions → numeric values in centimeters

4. **Normalization**
   - Techniques (e.g., oil, ink, watercolor)
   - Supports (canvas, paper, wood, etc.)
   - Artwork types
   - Countries and nationalities

5. **Integration**
   - Aligning columns across datasets
   - Concatenating into a single DataFrame

