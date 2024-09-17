from pydantic import BaseModel, Field
from typing import Union, List, Literal

# Define the classes for the tech classification
# 1. Advanced Computing, AI, and Information Technologies
class HPC(BaseModel):
    subtopic: Literal["High-Performance Computing"] = "High-Performance Computing"
    specifics: List[Literal['Supercomputing', 'Edge and Cloud Computing', 'Data Storage Processing Analysis', 'Quantum Computing']] = \
        Field(..., description="Relevant specific(s) on supercomputing, edge and cloud computing, data storage processing analysis, or quantum computing")

class AI(BaseModel):
    subtopic: Literal["AI and ML"] = "Artificial Intelligence (AI) and Machine Learning"
    specifics: List[Literal['Machine Learning', 'Sensory Perception', 'Planning Reasoning Decision Making', 'Safe Secure Green AI', 'Edge AI', 'Ethical AI']] = \
        Field(..., description="Relevant specific(s) on machine learning, sensory perception, planning reasoning decision making, safe secure green AI, edge AI, or ethical AI")

class BigData(BaseModel):
    subtopic: Literal["Big Data and Analytics"] = "Big Data and Analytics"
    specifics: List[Literal['Big Data Analytics', 'Data Fusion System Integration', 'Digital Twins']] = \
        Field(..., description="Relevant specific(s) on big data analytics, data fusion system integration, or digital twins")

class WearableProgrammableEnvironments(BaseModel):
    subtopic: Literal["Wearable and Programmable Environments"] = "Wearable and Programmable Environments"
    specifics: List[Literal['Wearable Computing', 'Programmable Wireless Environments', 'Human Machine Interfaces']] = \
        Field(..., description="Relevant specific(s) on wearable computing, programmable wireless environments, or human machine interfaces")

class Cybersecurity(BaseModel):
    subtopic: Literal["Cybersecurity and Cyber Defense"] = "Cybersecurity and Cyber Defense"
    specifics: List[Literal['Cyber Defense Situation Awareness', 'Autonomous Cyber Response', 'Quantum Cryptography', 'Cross Domain Cyber Operations']] = \
        Field(..., description="Relevant specific(s) on cyber defense situation awareness, autonomous cyber response, quantum cryptography, or cross domain cyber operations")

# 2. Advanced Materials and Manufacturing
class MaterialsScienceEngineering(BaseModel):
    subtopic: Literal['Materials Science and Engineering'] = "Materials Science and Engineering"
    specifics: List[Literal['Nanomaterials Atomic Scale Manufacturing', 'Superconductors 2D Quantum Materials', 'Advanced Composites Hybrids Metamaterials']] = \
        Field(..., description="Relevant specific(s) on nanomaterials atomic scale manufacturing, superconductors 2D quantum materials, or advanced composites hybrids metamaterials")

class SpecializedSmartMaterials(BaseModel):
    subtopic: Literal['Specialized and Smart Materials'] = "Specialized and Smart Materials"
    specifics: List[Literal['Biomaterials Bio Inspired Smart Materials', 'Materials Extreme Environments', 'Surface Engineering Smart Textiles']] = \
        Field(..., description="Relevant specific(s) on biomaterials bio inspired smart materials, materials extreme environments, or surface engineering smart textiles")

class AdvancedManufacturingProcesses(BaseModel):
    subtopic: Literal['Advanced Manufacturing Processes'] = "Advanced Manufacturing Processes"
    specifics: List[Literal['Additive Nanomanufacturing', 'Clean Sustainable Smart Manufacturing', 'Computational Design Materials Modeling']] = \
        Field(..., description="Relevant specific(s) on additive nanomanufacturing, clean sustainable smart manufacturing, or computational design materials modeling")

# 3. Energy Systems and Propulsion Technologies
class RenewableEnergyStorage(BaseModel):
    subtopic: Literal['Renewable Energy and Storage'] = "Renewable Energy and Storage"   
    specifics: List[Literal['Advanced Nuclear Renewable Energy', 'Advanced Battery Energy Storage', 'Solar Wind Alternative Energy']] = \
        Field(..., description="Relevant specific(s) on advanced nuclear renewable energy, advanced battery energy storage, or solar wind alternative energy")

class AdvancedPropulsionSystems(BaseModel):
    subtopic: Literal['Advanced Propulsion Systems'] = "Advanced Propulsion Systems"
    specifics: List[Literal['Hypersonics Advanced Gas Turbine', 'Electric Autonomous Vehicles', 'High Performance Aerospace Maritime Propulsion']] = \
        Field(..., description="Relevant specific(s) on hypersonics advanced gas turbine, electric autonomous vehicles, or high performance aerospace maritime propulsion")

# 4. Sensors, Electronics, and Communication
class AdvancedSensingImaging(BaseModel):
    subtopic: Literal['Advanced Sensing and Imaging'] = "Advanced Sensing and Imaging"
    specifics: List[Literal['Multispectral Hyperspectral Imaging', 'Lidar Radar Remote Sensing', 'Adaptive Optics 3D Tracking']] = \
        Field(..., description="Relevant specific(s) on multispectral hyperspectral imaging, lidar radar remote sensing, or adaptive optics 3D tracking")

class ElectronicsSemiconductors(BaseModel):
    subtopic: Literal['Electronics and Semiconductors'] = "Electronics and Semiconductors"
    specifics: List[Literal['Microelectronics Spintronics Twistronics', 'Optoelectronic RF Photonic Systems']] = \
        Field(..., description="Relevant specific(s) on microelectronics spintronics twistronics, or optoelectronic RF photonic systems")

class CommunicationNetworking(BaseModel):
    subtopic: Literal['Communication and Networking'] = "Communication and Networking"
    specifics: List[Literal['Quantum Information Communication', 'Advanced Wireless Networks', 'Tactical Cloud IoT Defense']] = \
        Field(..., description="Relevant specific(s) on quantum information communication, advanced wireless networks, or tactical cloud IoT defense")

# 5. Autonomous Systems and Robotics Technologies
class SurfaceAirMaritimeSpaceRobotics(BaseModel):
    subtopic: Literal['Surface, Air, Maritime, and Space Robotics'] = "Surface, Air, Maritime, and Space Robotics"
    specifics: List[Literal['Surface Robotics', 'Air Robotics', 'Maritime Robotics', 'Space Robotics']] = \
        Field(..., description="Relevant specific(s) on surface robotics, air robotics, maritime robotics, or space robotics")

class HumanMachineTeaming(BaseModel):
    subtopic: Literal['Human-Machine Teaming and Interfaces'] = "Human-Machine Teaming and Interfaces"
    specifics: List[Literal['Collaborative Robotics', 'Wearable Robotic Suits', 'Virtual Reality Robot Control', 'Brain Computer Interfaces']] = \
        Field(..., description="Relevant specific(s) on collaborative robotics, wearable robotic suits, virtual reality robot control, or brain computer interfaces")

class AutonomousNavigation(BaseModel):
    subtopic: Literal['Autonomous Navigation'] = "Autonomous Navigation"
    specifics: List[Literal['Advanced 3D Sensing', 'AI Path Planning', 'Swarm Robotics']] = \
        Field(..., description="Relevant specific(s) on advanced 3D sensing, AI path planning, or swarm robotics")

# 6. Space and Aerospace Technologies
class SatelliteTechnologies(BaseModel):
    subtopic: Literal["Satellite Technologies and Launch Vehicles"] = "Satellite Technologies and Launch Vehicles"
    specifics: List[Literal['Small Affordable Satellites', 'Reusable Rockets', 'New Propulsion Systems', 'Global Internet Satellites']] = \
        Field(..., description="Relevant specific(s) on small affordable satellites, reusable rockets, new propulsion systems, or global internet satellites")

class OnOrbitServices(BaseModel):
    subtopic: Literal["On-Orbit Servicing, Assembly, and Manufacturing"] = "On-Orbit Servicing, Assembly, and Manufacturing"
    specifics: List[Literal['Satellite Servicing Robots', 'Orbital Construction', 'Space 3D Printing']] = \
        Field(..., description="Relevant specific(s) on satellite servicing robots, orbital construction, or space 3D printing")

class SpaceSituationalAwareness(BaseModel):
    subtopic: Literal["Space Situational Awareness and PNT Systems"] = "Space Situational Awareness and PNT Systems"
    specifics: List[Literal['Space Debris Tracking', 'Space Weather Monitoring', 'Improved GPS Systems', 'AI Space Traffic Management']] = \
        Field(..., description="Relevant specific(s) on space debris tracking, space weather monitoring, improved GPS systems, or AI space traffic management")

# 7. Biotechnology, Medical, and Human Performance Technologies
class BiotechnologySyntheticBiology(BaseModel):
    subtopic: Literal['Biotechnology and Synthetic Biology'] = "Biotechnology and Synthetic Biology"
    specifics: List[Literal['Genome Protein Engineering', 'Biomanufacturing Bioprocessing', 'Advanced Diagnostics Therapeutics Biodefense']] = \
        Field(..., description="Relevant specific(s) on genome protein engineering, biomanufacturing bioprocessing, or advanced diagnostics therapeutics biodefense")

class HumanPerformanceEnhancement(BaseModel):
    subtopic: Literal['Human Performance Enhancement'] = "Human Performance Enhancement"
    specifics: List[Literal['Cognitive Science Neurotechnology', 'Performance Monitoring Optimization', 'Advanced Human Computer Interaction']] = \
        Field(..., description="Relevant specific(s) on cognitive science neurotechnology, performance monitoring optimization, or advanced human computer interaction")

class DefenseSecurityTechnologies(BaseModel):
    subtopic: Literal['Defense and Security Technologies'] = "Defense and Security Technologies"
    specifics: List[Literal['Directed Energy Advanced Munitions', 'CBRN Detection Protection', 'Signature Management Stealth', 'Electronic Warfare Cyber Defense']] = \
        Field(..., description="Relevant specific(s) on directed energy advanced munitions, CBRN detection protection, signature management stealth, or electronic warfare cyber defense")

# 8. Defense, Security, and Societal Technologies
class SimulationModelingTraining(BaseModel):
    subtopic: Literal['Simulation, Modeling, and Training'] = "Simulation, Modeling, and Training"    
    specifics: List[Literal['AI Driven Simulation Decision Support', 'Immersive Technologies Training', 'Integrated Live Virtual Constructive Simulation']] = \
        Field(..., description="Relevant specific(s) on AI driven simulation decision support, immersive technologies training, or integrated live virtual constructive simulation")

class SocietalIssuesEthicalTechnologies(BaseModel):
    subtopic: Literal['Societal Issues and Ethical Technologies'] = "Societal Issues and Ethical Technologies"
    specifics: List[Literal['AI Ethics Fake News Detection', 'Misinfodemics Assessment', 'Resilient Adaptive Systems']] = \
        Field(..., description="Relevant specific(s) on AI Ethics Fake News Detection, Misinfodemics Assessment, or Resilient Adaptive Systems on handling mis/dis/mal-information")

# 9. Environmental and Sustainability Technologies
class SustainClimateTechnologies(BaseModel):
    subtopic: Literal['Sustainablity and Climate Technologies'] = "Sustainable and Climate Technologies"
    specifics: List[Literal['Climate Change Mitigation Adaptation', 'Pollution Detection, Remediation, and Microplastics Removal', 'Circular Economy and Sustainable Agriculture']] = \
        Field(..., description="Relevant specific(s) on climate change mitigation adaptation, pollution detection, remediation, and microplastics removal, or circular economy and sustainable agriculture")

class EmergingEnvSol(BaseModel):
    subtopic: Literal['Emerging Environmental Solutions'] = "Emerging Environmental Solutions"
    specifics: List[Literal['Agrophotovoltaics and Nanoagriculture', 'Biomass Gasification and Interfacial Solar Evaporators', 'Plastic Chemical Upcycling and Energy Harvesting']] = \
        Field(..., description="Relevant specific(s) on agrophotovoltaics and nanoagriculture, biomass gasification and interfacial solar evaporators, or plastic chemical upcycling and energy harvesting")
    
    
# Consolidate all the sub-topics into topic
class AdvanceComputingAI(BaseModel):
    """
    The technology on *Advanced Computing, AI, and Information Technologies* is a topic, which cover the following sub-topics: High-Performance Computing (HPC), Artificial Intelligence (AI) and Machine Learning, Big Data and Analytics, Wearable and Programmable Environments, and Cybersecurity and Cyber Defense.
    If none of the sub-topics are selected, the topic will be classified as `None`.
    """
    adv_computing_ai: None|List[Union[HPC, AI, BigData, WearableProgrammableEnvironments, Cybersecurity]] = Field(..., description="The technology topics on Advanced Computing, AI, and Information Technologies")

class AdvancedMaterialsManufacturing(BaseModel):
    """
    The technology on *Advanced Materials and Manufacturing* is a topic, which cover the following sub-topics: Materials Science and Engineering, Specialized and Smart Materials, and Advanced Manufacturing Processes.
    If none of the topics are selected, the category will be classified as `None`.
    """
    adv_materials_manufacture: None | List[Union[MaterialsScienceEngineering, SpecializedSmartMaterials, AdvancedManufacturingProcesses]] = Field(..., description="The technology topics on Advanced Materials and Manufacturing")

class EnergySystemsPropulsion(BaseModel):
    """
    The technology on *Energy Systems and Propulsion* is a topic, which cover the following sub-topics: Renewable Energy and Storage, and Advanced Propulsion Systems.
    """
    energy_sys_propulsion: None | List[Union[RenewableEnergyStorage, AdvancedPropulsionSystems]] = Field(..., description="The technology topics on Energy Systems and Propulsion Technologies")

class SensorsElectronicsCommunication(BaseModel):
    """
    The technology on *Sensors, Electronics, and Communication* is a topic, which cover the following sub-topics: Advanced Sensing and Imaging, Electronics and Semiconductors, and Communication and Networking. Can be None if not applicable.
    If none of the sub-topics are selected, the topic will be classified as `None`.
    """
    sensors_electronics_comm: None | List[Union[AdvancedSensingImaging, ElectronicsSemiconductors, CommunicationNetworking]] = Field(..., description="The technology topics on Sensors, Electronics, and Communication")

class AutonomousSystemsRobotics(BaseModel):
    """
    The technology on *Autonomous Systems and Robotics* is a topic, which cover the following sub-topics: Surface, Air, Maritime, and Space Robotics, Human-Machine Teaming and Interfaces, and Autonomous Navigation and Decision-Making.
    """
    auto_systems_robotics: None | List[Union[SurfaceAirMaritimeSpaceRobotics, HumanMachineTeaming, AutonomousNavigation]] = Field(..., description="The technology topics on Autonomous Systems and Robotics Technologies")

class SpaceAerospaceTechnologies(BaseModel):
    """
    The technology on *Space and Aerospace Technologies* is a topic, which cover the following sub-topics: Satellite Technologies and Launch Vehicles, On-Orbit Servicing, Assembly, and Manufacturing, and Space Situational Awareness and PNT Systems.
    If none of the sub-topics are selected, the topic will be classified as `None`.
    """
    space_aerospace_tech: None | List[Union[SatelliteTechnologies, OnOrbitServices, SpaceSituationalAwareness]] = Field(..., description="The technology topics on Space and Aerospace Technologies")

class BiotechMedicalHumanPerformance(BaseModel):
    """
    The technology on *Biotechnology, Medical, and Human Performance* is a topic, which cover the following sub-topics: Biotechnology and Synthetic Biology, and Human Performance.
    If none of the sub-topics are selected, the topic will be classified as `None`.
    """
    biotech_med_human_perf: None | List[Union[BiotechnologySyntheticBiology, HumanPerformanceEnhancement]] = Field(..., description="The technology topics on Biotechnology, Medical, and Human Performance Technologies")

class DefenseSecuritySocietalTech(BaseModel):
    """
    The technology on *Defense, Security, and Societal* is a topic, which cover the following sub-topics: Defense and Security Technologies, Simulation, Modeling, and Training, and Societal Issues and Ethical Technologies.
    """
    def_sec_societal_tech: None | List[Union[DefenseSecurityTechnologies, SimulationModelingTraining, SocietalIssuesEthicalTechnologies]] = Field(..., description="The technology topics on Defense, Security, and Societal Technologies")

class EnvironmentalSustainabilityTech(BaseModel):
    """
    The technology on *Environmental and Sustainability* is a topic, which cover the following sub-topics: Sustainability and Climate Technologies, and Emerging Environmental Solutions.
    If none of the sub-topics are selected, the topic will be classified as `None`.
    """
    env_sustain_tech: None | List[Union[SustainClimateTechnologies, EmergingEnvSol]] = Field(..., description="The technology topics on Environmental and Sustainability Technologies")

# Define all the technology classes into a single requirement
class TechnologiesClassifier(BaseModel):
    """
    The technology list for classifying a company/individual based on the technology topics on:
    - Advanced Computing, AI, and Information Technologies
    - Advanced Materials and Manufacturing
    - Energy Systems and Propulsion Technologies
    - Sensors, Electronics, and Communication Technologies
    - Autonomous Systems and Robotics Technologies
    - Space and Aerospace Technologies
    - Biotechnology, Medical, and Human Performance Technologies
    - Defense, Security, and Societal Technologies
    - Environmental and Sustainability Technologies
    """
    entity_name: str = Field(..., description="The name of the company or individual to classify based on the technology topics and sub-topics")
    technologies_applicable: None | List[Union[AdvanceComputingAI, 
                                               AdvancedMaterialsManufacturing,
                                               EnergySystemsPropulsion,
                                               SensorsElectronicsCommunication,
                                               AutonomousSystemsRobotics,
                                               SpaceAerospaceTechnologies,
                                               BiotechMedicalHumanPerformance,
                                               DefenseSecuritySocietalTech,
                                               EnvironmentalSustainabilityTech]] = \
    Field(..., description="The technology list for classifying a company/individual based on the technology topics and sub-topics")
    
classify_technologies = {
    "type": "function",
    "function": {
        "name": "classify_technologies",
        "description": "Classify a company/individual based on the technologist list of topics and sub-topics.",
        "parameters": TechnologiesClassifier.model_json_schema()
    }
}