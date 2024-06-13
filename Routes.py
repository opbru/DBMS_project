from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Component, CPU, COMPUTER_TYPE, MB, RAM, SSD, HDD, GPU, PSU, CHASSIS, User, UserSelections
from Utils import get_compatible_mbs, get_compatible_rams, get_compatible_chassis
from flask import make_response


routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()




@routes.route('/register', methods=['POST'])

def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(f"Received data: email={email}, password={password}")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # verify user creation
    user = User.query.filter_by(email=email).first()

    if user:
        print(f"User registered: {user.email}")
    else:
        print("User registration failed.")

    return jsonify({"message": "User registered successfully"}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'email': user.email})
        session['user_id'] = user.id #storing user id in session
        print(f"Login successful for user: {user.email}")
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@routes.route('/set_budget_and_type', methods=['POST'])
@jwt_required()
def set_budget_and_type():
    data = request.get_json()
    print(f"Received data: {data}")
    budget = data['budget']
    computer_type = data['computer_type']
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    user.budget = budget
    user.computer_type = computer_type
    db.session.commit()
    return jsonify({"message": "Budget and component type set successfully"}), 200

@routes.route('/get_cpu_options', methods=['GET'])
@jwt_required()
def get_cpu_options():
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        print(f"User: {user.email}, Computer Type: {user.computer_type}")

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if computer_type is None:
            print(f"No computer type found for {user.computer_type}")
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget
        max_cpu_price = budget * computer_type.cpu_ratio
        print(f"Budget: {budget}, CPU Ratio: {computer_type.cpu_ratio}")


        cpu_options = CPU.query.join(Component, CPU.component_ID == Component.ID)\
                        .filter(Component.price <= max_cpu_price)\
                        .order_by(Component.price.desc()).all()

        result = []
        for cpu in cpu_options:
            component = Component.query.get(cpu.component_ID)
            result.append({
                "name": cpu.name,
                "price": component.price,
                "benchmark": cpu.benchmark,
                "id" : cpu.id
            })

        response = make_response(jsonify(result), 200)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    except Exception as e:
        print(f"Exception occurred in get_cpu_options: {e}")
        return jsonify({"message": "An error occurred"}), 500



@routes.route('/select_cpu/<cpu_id>', methods=['POST'])
@jwt_required()
def select_cpu(cpu_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retrieve the CPU object using the cpu_id
    cpu = CPU.query.get(cpu_id)
    if not cpu:
        return jsonify({"message": "CPU not found"}), 404

    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='cpu').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='cpu', component_id=cpu.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "CPU selected successfully"}), 200


@routes.route('/get_mb_options/<cpu_id>', methods=['GET'])
@jwt_required()
def get_mb_options(cpu_id):
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # cpu_id = session.get('selected_cpu_id')
        if not cpu_id:
            return jsonify({"message": "CPU not selected"}), 400

        cpu = CPU.query.get(cpu_id)

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget

        compatible_mbs = get_compatible_mbs(cpu.socket)

        # Sort compatible_mbs by price in descending order
        compatible_mbs_filtered_sorted = [
            mb for mb in compatible_mbs
            if Component.query.get(mb.component_ID).price <= budget * computer_type.mb_ratio
        ]
        compatible_mbs_filtered_sorted.sort(key=lambda mb: Component.query.get(mb.component_ID).price, reverse=True)

        result = []
        for mb in compatible_mbs_filtered_sorted:
            component = Component.query.get(mb.component_ID)
            result.append({
                "name": mb.name,
                "price": component.price,
                "id" : mb.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_mb_options: {e}")
        return jsonify({"message": "An error occurred"}), 500


@routes.route('/select_mb/<mb_id>', methods=['POST'])
@jwt_required()
def select_mb(mb_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    mb = MB.query.get(mb_id)
    if not mb:
        return jsonify({"message": "MB not found"}), 404
    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='mb').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='mb', component_id=mb.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "MB selected successfully"}), 200


@routes.route('/get_ram_options/<mb_id>', methods=['GET'])
@jwt_required()
def get_ram_options(mb_id):
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # mb_id = session.get('selected_mb_id')
        if not mb_id:
            return jsonify({"message": "Motherboard not selected"}), 400

        mb = MB.query.get(mb_id)
        if not mb:
            return jsonify({"message": "Motherboard not found"}), 404

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget

        compatible_rams = get_compatible_rams(mb.interface)
        compatible_rams_filtered_sorted = [
            ram for ram in compatible_rams
            if Component.query.get(ram.component_ID).price <= budget * computer_type.ram_ratio
        ]
        compatible_rams_filtered_sorted.sort(key=lambda ram: Component.query.get(ram.component_ID).price, reverse=True)

        result = []
        for ram in compatible_rams_filtered_sorted:
            component = Component.query.get(ram.component_ID)
            result.append({
                "name": ram.name,
                "price": component.price,
                "id" : ram.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_ram_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_ram/<ram_id>', methods=['POST'])
@jwt_required()
def select_ram(ram_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    ram = RAM.query.get(ram_id)
    if not ram:
        return jsonify({"message": "RAM not found"}), 404
    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='ram').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='ram', component_id=ram.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "RAM selected successfully"}), 200

@routes.route('/get_ssd_options', methods=['GET'])
@jwt_required()
def get_ssd_options():
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget

        ssd_options = SSD.query.join(Component, SSD.component_ID == Component.ID)\
                        .filter(Component.price <= budget * computer_type.ssd_ratio)\
                        .order_by(Component.price.desc()).all()

        result = []
        for ssd in ssd_options:
            component = Component.query.get(ssd.component_ID)
            result.append({
                "name": ssd.name,
                "price": component.price,
                "id" : ssd.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_ssd_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_ssd/<ssd_id>', methods=['POST'])
@jwt_required()
def select_ssd(ssd_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    ssd = SSD.query.get(ssd_id)
    if not ssd:
        return jsonify({"message": "SSD not found"}), 404
    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='ssd').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='ssd', component_id=ssd.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "SSD selected successfully"}), 200

@routes.route('/get_hdd_options', methods=['GET'])
@jwt_required()
def get_hdd_options():
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404



        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget
        print(f"Budget: {budget}, HDD Ratio: {computer_type.hdd_ratio}")

        hdd_options = HDD.query.join(Component, HDD.component_ID == Component.ID)\
                        .filter(Component.price <= budget * computer_type.hdd_ratio)\
                        .order_by(Component.price.desc()).all()

        result = []
        for hdd in hdd_options:
            component = Component.query.get(hdd.component_ID)
            result.append({
                "name": hdd.name,
                "price": component.price,
                "id" : hdd.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_hdd_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_hdd/<hdd_id>', methods=['POST'])
@jwt_required()
def select_hdd(hdd_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    hdd = HDD.query.get(hdd_id)
    if not hdd:
        return jsonify({"message": "HDD not found"}), 404

    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='hdd').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='hdd', component_id=hdd.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "HDD selected successfully"}), 200

@routes.route('/get_gpu_options', methods=['GET'])
@jwt_required()
def get_gpu_options():
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget

        gpu_options = GPU.query.join(Component, GPU.component_ID == Component.ID)\
                        .filter(Component.price <= budget * computer_type.gpu_ratio)\
                        .order_by(Component.price.desc()).all()

        result = []
        for gpu in gpu_options:
            component = Component.query.get(gpu.component_ID)
            result.append({
                "name": gpu.name,
                "price": component.price,
                "benchmark": gpu.benchmark,
                "id" : gpu.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_gpu_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_gpu/<gpu_id>', methods=['POST'])
@jwt_required()
def select_gpu(gpu_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    gpu = GPU.query.get(gpu_id)
    if not gpu:
        return jsonify({"message": "GPU not found"}), 404

    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='gpu').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='gpu', component_id=gpu.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "GPU selected successfully"}), 200


@routes.route('/get_psu_options', methods=['GET'])
@jwt_required()
def get_psu_options():
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        budget = user.budget

        psu_options = PSU.query.join(Component, PSU.component_ID == Component.ID)\
                        .filter(Component.price <= budget * computer_type.psu_ratio)\
                        .order_by(Component.price.desc()).all()

        result = []
        for psu in psu_options:
            component = Component.query.get(psu.component_ID)
            result.append({
                "name": psu.name,
                "price": component.price,
                "id" : psu.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_psu_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_psu/<psu_id>', methods=['POST'])
@jwt_required()
def select_psu(psu_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    psu = PSU.query.get(psu_id)
    if not psu:
        return jsonify({"message": "PSU not found"}), 404

    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='psu').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='psu', component_id=psu.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "PSU selected successfully"}), 200




@routes.route('/get_chassis_options/<mb_id>/<gpu_id>', methods=['GET'])
@jwt_required()
def get_chassis_options(mb_id, gpu_id):
    try:
        user = User.query.filter_by(email=get_jwt_identity()['email']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        computer_type = COMPUTER_TYPE.query.filter_by(name=user.computer_type).first()
        if not computer_type:
            return jsonify({"message": "Invalid computer type"}), 400

        # mb_id = session.get('selected_mb_id')
        # gpu_id = session.get('selected_gpu_id')
        budget = user.budget

        mb = MB.query.get(mb_id)
        if not mb:
            return jsonify({"message": "Motherboard not found"}), 404

        gpu = GPU.query.get(gpu_id)
        if not gpu:
            return jsonify({"message": "GPU not found"}), 404

        compatible_chassis = get_compatible_chassis(mb.form_factor, gpu.size)

        # Filter by budget and sort by price descending
        compatible_chassis_filtered_sorted = [
            chassis for chassis in compatible_chassis
            if Component.query.get(chassis.component_ID).price <= budget * computer_type.chassis_ratio
        ]
        compatible_chassis_filtered_sorted.sort(key=lambda chassis: Component.query.get(chassis.component_ID).price, reverse=True)

        result = []
        for chassis in compatible_chassis_filtered_sorted:
            component = Component.query.get(chassis.component_ID)
            result.append({
                "name": chassis.name,
                "price": component.price,
                "id" : chassis.id
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Exception occurred in get_chassis_options: {e}")
        return jsonify({"message": "An error occurred"}), 500

@routes.route('/select_chassis/<chassis_id>', methods=['POST'])
@jwt_required()
def select_chassis(chassis_id):
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    chassis = CHASSIS.query.get(chassis_id)
    if not chassis:
        return jsonify({"message": "CHASSIS not found"}), 404

    # Remove any previous selection of the same type
    UserSelections.query.filter_by(user_id=user.id, component_type='chassis').delete()

    # Add new selection
    new_selection = UserSelections(user_id=user.id, component_type='chassis', component_id=chassis.component_ID)
    db.session.add(new_selection)
    db.session.commit()

    return jsonify({"message": "CHASSIS selected successfully"}), 200



@routes.route('/finalize_selection', methods=['POST'])
@jwt_required()
def finalize_selection():
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    selected_components = UserSelections.query.filter_by(user_id=user.id).all()

    total_price = 0
    components_list = []

    for selection in selected_components:
        component = Component.query.get(selection.component_id)
        if component:
            components_list.append({
                "type": selection.component_type,
                "name": component.name,
                "price": component.price
            })
            total_price += component.price

    return jsonify({"selected_components": components_list, "total_price": total_price}), 200

@routes.route('/recommend_gpu', methods=['GET'])
@jwt_required()
def recommend_gpu():
    user = User.query.filter_by(email=get_jwt_identity()['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    total_price = 0
    selected_components = UserSelections.query.filter_by(user_id=user.id).all()

    print(f"Selected components: {selected_components}")


    for selection in selected_components:
        component = Component.query.get(selection.component_id)
        if component:
            total_price += component.price

    remaining_budget = user.budget - total_price
    current_gpu_selection = UserSelections.query.filter_by(user_id=user.id, component_type='gpu').first()
    current_gpu = GPU.query.get(current_gpu_selection.component_id) if current_gpu_selection else None
    if current_gpu:
        print(f"Current GPU: {current_gpu.name}, Benchmark: {current_gpu.benchmark}, Component ID: {current_gpu.component_ID}")
    else:
        print("No current GPU selected")
    better_gpu = GPU.query.join(Component, GPU.component_ID == Component.ID) \
                          .filter(Component.price <= remaining_budget) \
                          .filter(GPU.benchmark > (current_gpu.benchmark if current_gpu else 0)) \
                          .order_by(GPU.benchmark.desc()).first()

    if not better_gpu:
        return jsonify({"message": "No better GPU found within remaining budget"}), 200

    better_gpu_component = Component.query.get(better_gpu.component_ID)
    current_gpu_component = Component.query.get(current_gpu.component_ID) if current_gpu else None

    print(f"Better GPU: {better_gpu.name}, Price: {better_gpu_component.price}, Benchmark: {better_gpu.benchmark}")
    print(f"Current GPU Price: {current_gpu_component.price if current_gpu_component else 0}, Benchmark: {current_gpu.benchmark if current_gpu else 0}")

    more_price = better_gpu_component.price - (current_gpu_component.price if current_gpu_component else 0)
    more_benchmark = better_gpu.benchmark - (current_gpu.benchmark if current_gpu else 0)
    cp_ratio = more_benchmark / more_price if more_price > 0 else float('inf')

    print(f"More Price: {more_price}, More Benchmark: {more_benchmark}, C/P Ratio: {cp_ratio}")


    return jsonify({
        "better_gpu_name": better_gpu.name,
        "more_price": more_price,
        "more_benchmark": more_benchmark,
        "cp_ratio": cp_ratio,
        "id": better_gpu.id
    }), 200



@routes.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Fetch all computer types to test connection
        computer_types = COMPUTER_TYPE.query.all()
        return jsonify([ct.name for ct in computer_types]), 200
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"message": "An error occurred connecting to the database"}), 500