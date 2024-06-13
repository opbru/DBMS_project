from models import CPU, MB, RAM, SSD, HDD, GPU, PSU, CHASSIS, Component, User, COMPUTER_TYPE

def get_compatible_mbs(cpu_socket):
    return MB.query.filter_by(socket=cpu_socket).all()

def get_compatible_rams(mb_interface):
    return RAM.query.filter_by(interface=mb_interface).all()

def get_compatible_chassis(mb_form_factor, gpu_size):
    return CHASSIS.query.filter_by(mb_form_factor=mb_form_factor).filter(CHASSIS.GPU_size >= gpu_size).all()

# def get_recommended_components(user_id):
#     user = User.query.get(user_id)
#     computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
    
#     if not user or not computer_type:
#         return None
    
#     budget = user.budget
#     component_recommendations = {}

#     component_recommendations['CPU'] = CPU.query.filter(CPU.component_ID == Component.ID, Component.price <= budget * computer_type.cpu_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['MB'] = MB.query.filter(MB.component_ID == Component.ID, Component.price <= budget * computer_type.mb_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['RAM'] = RAM.query.filter(RAM.component_ID == Component.ID, Component.price <= budget * computer_type.ram_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['SSD'] = SSD.query.filter(SSD.component_ID == Component.ID, Component.price <= budget * computer_type.ssd_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['HDD'] = HDD.query.filter(HDD.component_ID == Component.ID, Component.price <= budget * computer_type.hdd_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['GPU'] = GPU.query.filter(GPU.component_ID == Component.ID, Component.price <= budget * computer_type.gpu_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['CHASSIS'] = CHASSIS.query.filter(CHASSIS.component_ID == Component.ID, Component.price <= budget * computer_type.chassis_ratio).order_by(Component.price.desc()).first()
#     component_recommendations['PSU'] = PSU.query.filter(PSU.component_ID == Component.ID, Component.price <= budget * computer_type.psu_ratio).order_by(Component.price.desc()).first()

#     return component_recommendations
