# L'Atelier de Bing - Engineering Tool

## Project Overview
An engineering tool platform with multiple specialized tools for motor specification management and visualization.

## Current Development Focus: VDG Motor Spec Tool

### Project Structure
- **APP Folder**: Contains all application-related files
- **First Tool**: `vdg_motor_spec` - Motor specification management system

### Vdg_Motor_Spec Tool - Requirements

#### Feature: Motor Record Navigation & Viewing
- **Trigger**: Clicking a record in the list
- **Action**: Navigates to a new page called `motor_view`
- **Function**: Pulls the selected motor record and displays its specifications

#### Motor View Page Layout & Design
1. **Specification Groups**: Split motor specifications into two groups based on unit type:
   - **Metric Group**: All specifications using metric units
   - **Imperial Group**: All specifications using imperial units

2. **Page Layout**:
   - Left area: Display specification groups (Metric & Imperial)
   - **Middle Right Area**: Reserved space for motor visualization/photo
   - Flexible layout to accommodate photo placement

#### Visualization
- Reserved middle-right area for motor photo/image
- Will be populated with visual representation of the selected motor

### Development Status
- [ ] vdg_motor_spec list view component
- [ ] motor_view detail page component
- [ ] Specification data model with unit classification
- [ ] Navigation between list and detail views
- [ ] Metric/Imperial grouping logic
- [ ] Photo visualization area implementation

---
**Session Date**: 2026-06-11  
**Developer**: Ben2008
