from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)

# =========================================================
# FLASK SECRET KEY
# =========================================================

app.secret_key = os.getenv("SECRET_KEY", "local-dev-key-change-before-deploy")


# =========================================================
# MYSQL DATABASE CONNECTION
# =========================================================

DB_CONFIG = {
    # Locally these defaults connect to MySQL on your computer.
    # On Railway, set the AGRISMART_DB_* variables in the service settings.
    "host": os.getenv("AGRISMART_DB_HOST", "localhost"),
    "user": os.getenv("AGRISMART_DB_USER", "root"),
    "password": os.getenv("AGRISMART_DB_PASSWORD", ""),
    "database": os.getenv("AGRISMART_DB_NAME", "agrismart"),
    "port": int(os.getenv("AGRISMART_DB_PORT", "3306"))
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )

        return connection

    except Error as e:
        print("MySQL Connection Error:", e)
        return None


# =========================================================
# LOGIN PROTECTION
# =========================================================

@app.before_request
def login_required():

    allowed_endpoints = {
        "login",
        "register",
        "logout",
        "static"
    }

    if request.endpoint in allowed_endpoints:
        return None

    if request.endpoint is None:
        return None

    if "user_id" not in session:
        return redirect(url_for("login"))

    return None


# =========================================================
# ADMIN CHECK
# =========================================================

def is_admin():

    return (
        "user_id" in session
        and session.get("user_type", "").lower() == "admin"
    )


# =========================================================
# CROP ICONS
# =========================================================

CROP_ICONS = {

    "Wheat": "🌾",
    "Rice": "🌾",
    "Cotton": "🌿",
    "Maize": "🌽",
    "Sugarcane": "🎋",
    "Tomato": "🍅",
    "Potato": "🥔",
    "Soybean": "🌱",

    "Onion": "🧅",
    "Groundnut": "🥜",
    "Peanut": "🥜",
    "Carrot": "🥕",
    "Chilli": "🌶️",
    "Banana": "🍌",
    "Mango": "🥭",
    "Apple": "🍎"
}


# =========================================================
# CROP DESCRIPTIONS
# =========================================================

CROP_DESCRIPTIONS = {

    "Wheat":
        "An important Rabi crop grown mainly in cool and relatively dry conditions.",

    "Rice":
        "A major food crop requiring warm conditions and careful water management.",

    "Cotton":
        "A major commercial fibre crop requiring warm conditions and suitable soil.",

    "Maize":
        "A versatile cereal crop used for food, feed and industrial purposes.",

    "Sugarcane":
        "A commercial crop requiring warm conditions, fertile soil and adequate moisture.",

    "Tomato":
        "A popular vegetable crop requiring suitable temperature, sunlight and drainage.",

    "Potato":
        "An important tuber crop generally grown during cool growing conditions.",

    "Soybean":
        "An important Kharif oilseed and pulse crop suited to well-drained soil.",

    "Onion":
        "An important vegetable crop cultivated in different seasons depending on region.",

    "Groundnut":
        "An important oilseed crop that grows well in warm conditions and suitable soil."
}


# =========================================================
# DETAILED CROP ADVISORY
# =========================================================

CROP_ADVISORY = {

    "Wheat": {

        "overview":
            "Wheat is an important Rabi cereal crop. It generally performs well under cool growing conditions and requires a well-prepared field with good drainage.",

        "season":
            "Rabi season. Sowing time depends on local climate, variety and agricultural recommendations.",

        "sowing":
            "Use healthy and good-quality seed. Prepare a fine, level seedbed and maintain suitable spacing and sowing depth according to the selected variety.",

        "irrigation":
            "Provide irrigation according to soil moisture, rainfall and crop growth stage. Avoid unnecessary irrigation and waterlogging.",

        "fertilizer":
            "Nutrients should preferably be applied according to soil-test results and local agricultural recommendations. Nitrogen, phosphorus and potassium are important for balanced crop growth.",

        "nutrients":
            "Nitrogen supports vegetative growth, phosphorus supports root development and potassium contributes to plant strength and crop quality.",

        "pests":
            "Common problems may include aphids, termites and other field pests depending on location and season.",

        "diseases":
            "Rusts, powdery mildew and other fungal diseases may occur under favourable conditions.",

        "prevention":
            "Use healthy seed, maintain field sanitation, avoid excessive moisture and regularly inspect the crop for early signs of pests or disease.",

        "weeds":
            "Early weed management is important because weeds compete with wheat plants for water, nutrients and sunlight.",

        "harvesting":
            "Harvest when the crop reaches proper maturity and grains have sufficiently dried. Avoid unnecessary delay after maturity.",

        "storage":
            "Dry harvested grain properly and store it in a clean, dry and protected storage area.",

        "tips": [
            "Select a suitable variety for the local region.",
            "Use good-quality seed from a reliable source.",
            "Maintain proper soil moisture.",
            "Follow soil-test-based nutrient management.",
            "Monitor the crop regularly for pests and diseases."
        ]
    },


    "Rice": {

        "overview":
            "Rice is a major food crop that generally requires warm conditions and careful water management. Cultivation practices vary according to rice variety and production system.",

        "season":
            "Commonly cultivated during the Kharif season in many parts of India, although season varies by region.",

        "sowing":
            "Use healthy seed and follow the recommended nursery, transplanting or direct-seeding method suitable for the selected variety and local conditions.",

        "irrigation":
            "Maintain adequate moisture according to the production system. Avoid uncontrolled water use and follow efficient irrigation practices where possible.",

        "fertilizer":
            "Balanced nutrient management is important. Fertilizer application should preferably follow soil testing and recommendations for the selected variety and region.",

        "nutrients":
            "Nitrogen supports plant growth, phosphorus contributes to root development and potassium supports plant strength and grain development.",

        "pests":
            "Stem borers, leaf folders, planthoppers and other pests may affect rice depending on local conditions.",

        "diseases":
            "Blast, bacterial leaf-related diseases and sheath diseases can affect rice under favourable conditions.",

        "prevention":
            "Use healthy seed, maintain proper spacing, monitor fields regularly and avoid excessive nitrogen or unnecessary pesticide use.",

        "weeds":
            "Timely weed management is important, particularly during the early growth period.",

        "harvesting":
            "Harvest when the crop reaches maturity and most grains have developed the required maturity characteristics.",

        "storage":
            "Dry paddy properly before storage and protect stored grain from moisture, insects and rodents.",

        "tips": [
            "Use certified or quality seed where available.",
            "Maintain proper field and water management.",
            "Monitor pests regularly.",
            "Avoid excessive fertilizer application.",
            "Dry harvested grain properly before storage."
        ]
    },


    "Cotton": {

        "overview":
            "Cotton is an important commercial fibre crop that generally requires warm conditions, suitable soil and adequate moisture during important growth stages.",

        "season":
            "Generally grown as a Kharif crop in many Indian regions. Sowing period depends on rainfall and local conditions.",

        "sowing":
            "Select a suitable variety and use healthy seed. Maintain appropriate spacing according to the variety and recommended cultivation practice.",

        "irrigation":
            "Irrigation should be managed according to rainfall, soil type and crop growth stage. Avoid prolonged waterlogging.",

        "fertilizer":
            "Balanced nutrition is important. Apply nutrients according to soil-test results and crop recommendations.",

        "nutrients":
            "Nitrogen, phosphorus and potassium all contribute to crop development, while balanced nutrition supports flowering and boll development.",

        "pests":
            "Cotton can be affected by bollworms, sucking pests and other insects depending on the area.",

        "diseases":
            "Wilt, leaf-related diseases and other fungal or bacterial problems may occur depending on environmental conditions.",

        "prevention":
            "Inspect plants regularly, maintain field sanitation, use recommended varieties and follow integrated pest management practices.",

        "weeds":
            "Control weeds during early crop growth to reduce competition for nutrients, water and sunlight.",

        "harvesting":
            "Pick mature cotton bolls at the appropriate stage and avoid contamination with soil or other material.",

        "storage":
            "Keep harvested cotton clean and dry and protect it from moisture during storage.",

        "tips": [
            "Choose a suitable variety for local conditions.",
            "Maintain proper plant spacing.",
            "Monitor the crop regularly for sucking pests.",
            "Avoid waterlogging.",
            "Follow integrated pest management practices."
        ]
    },


    "Maize": {

        "overview":
            "Maize is a versatile cereal crop grown for food, animal feed and industrial uses. It performs well under warm conditions with good soil drainage.",

        "season":
            "Often grown during Kharif, Rabi or other seasons depending on region, irrigation and variety.",

        "sowing":
            "Use healthy seed and maintain suitable spacing and planting depth. Prepare a well-drained field before sowing.",

        "irrigation":
            "Provide adequate moisture during important growth stages while avoiding waterlogging.",

        "fertilizer":
            "Balanced fertilizer management is important. Nutrient application should be based on soil condition and local recommendations.",

        "nutrients":
            "Nitrogen supports vegetative growth, phosphorus supports roots and potassium contributes to plant strength and crop development.",

        "pests":
            "Fall armyworm, stem borers and other pests may affect maize in different areas.",

        "diseases":
            "Leaf blights, rust and other diseases may occur depending on environmental conditions.",

        "prevention":
            "Inspect plants frequently, maintain field hygiene, use healthy seed and follow recommended pest management practices.",

        "weeds":
            "Early weed control is important because maize can suffer from competition during the initial growth period.",

        "harvesting":
            "Harvest when ears and grains reach the recommended maturity stage and moisture is suitable for harvesting and storage.",

        "storage":
            "Dry maize properly and store it in a clean, dry and pest-protected location.",

        "tips": [
            "Use good-quality seed.",
            "Maintain proper plant spacing.",
            "Monitor for fall armyworm and other pests.",
            "Maintain adequate soil moisture.",
            "Dry grains properly before storage."
        ]
    },


    "Sugarcane": {

        "overview":
            "Sugarcane is a major commercial crop requiring warm conditions, fertile soil and sufficient moisture over a relatively long growing period.",

        "season":
            "Planting season varies by region and production system. Follow local agricultural recommendations.",

        "sowing":
            "Use healthy planting material and prepare the field properly. Good-quality setts or recommended planting material support better establishment.",

        "irrigation":
            "Sugarcane requires regular moisture, but excessive waterlogging should be avoided. Irrigation should consider rainfall and soil type.",

        "fertilizer":
            "Balanced nutrient management is important because sugarcane remains in the field for a long duration. Soil testing should guide fertilizer application.",

        "nutrients":
            "Nitrogen supports growth, phosphorus supports root development and potassium contributes to plant strength and crop development.",

        "pests":
            "Early shoot borer, stem borer and other pests can affect sugarcane depending on location.",

        "diseases":
            "Red rot, smut and other diseases may occur in susceptible varieties and favourable conditions.",

        "prevention":
            "Use healthy planting material, maintain field sanitation and inspect the crop regularly for pest and disease symptoms.",

        "weeds":
            "Weed control is important during early crop establishment because weeds compete strongly for resources.",

        "harvesting":
            "Harvest at suitable maturity according to variety and local recommendations. Proper harvesting helps maintain cane quality.",

        "storage":
            "Harvested cane should generally be processed promptly to reduce quality loss.",

        "tips": [
            "Use healthy planting material.",
            "Maintain proper irrigation.",
            "Avoid waterlogging.",
            "Monitor for borers and diseases.",
            "Follow recommended harvesting practices."
        ]
    },


    "Tomato": {

        "overview":
            "Tomato is an important vegetable crop requiring suitable temperature, good sunlight, fertile soil and effective water management.",

        "season":
            "Growing season varies considerably by region and climate. Follow local recommendations for nursery and transplanting.",

        "sowing":
            "Use healthy seed and raise quality seedlings. Transplant strong seedlings into well-prepared and well-drained soil.",

        "irrigation":
            "Maintain consistent soil moisture while avoiding excessive irrigation and waterlogging. Drip irrigation can improve water-use efficiency where available.",

        "fertilizer":
            "Apply balanced nutrients based on soil testing and crop requirements. Excess fertilizer should be avoided.",

        "nutrients":
            "Nitrogen supports vegetative growth, phosphorus contributes to root and reproductive development and potassium supports fruit quality.",

        "pests":
            "Fruit borer, whiteflies, aphids and other pests may affect tomato plants.",

        "diseases":
            "Early blight, late blight, wilt and viral diseases may occur depending on variety and environmental conditions.",

        "prevention":
            "Use healthy seedlings, maintain field sanitation, provide proper spacing and inspect plants frequently.",

        "weeds":
            "Regular weed management helps reduce competition and improves air circulation around plants.",

        "harvesting":
            "Harvest fruits according to the required maturity stage and intended market or use.",

        "storage":
            "Handle fruits carefully to reduce bruising and store them under suitable conditions for the intended storage period.",

        "tips": [
            "Use healthy seedlings.",
            "Maintain consistent soil moisture.",
            "Provide adequate sunlight.",
            "Monitor fruit borer and sucking pests.",
            "Remove severely affected plant material where appropriate."
        ]
    },


    "Potato": {

        "overview":
            "Potato is an important tuber crop generally grown under cool conditions. It performs well in loose, fertile and well-drained soil.",

        "season":
            "Commonly grown as a Rabi crop in many regions, although the season varies according to local climate.",

        "sowing":
            "Use healthy, disease-free seed tubers of suitable size and variety. Prepare loose soil to support tuber development.",

        "irrigation":
            "Maintain adequate moisture during tuber development while avoiding waterlogging.",

        "fertilizer":
            "Apply balanced nutrients based on soil testing and local recommendations. Nutrient needs vary with soil and variety.",

        "nutrients":
            "Balanced nitrogen, phosphorus and potassium support plant growth and tuber development.",

        "pests":
            "Potato tuber moth, aphids and other pests may affect the crop.",

        "diseases":
            "Late blight, early blight and bacterial or viral diseases may occur.",

        "prevention":
            "Use healthy seed tubers, maintain field hygiene, avoid excessive moisture and inspect plants regularly.",

        "weeds":
            "Timely weed control is important during early crop growth. Earthing-up also supports tuber development and crop management.",

        "harvesting":
            "Harvest when tubers reach suitable maturity and the crop shows appropriate maturity symptoms.",

        "storage":
            "Cure and store tubers in a cool, dry and well-ventilated environment suitable for potato storage.",

        "tips": [
            "Use healthy seed tubers.",
            "Avoid waterlogging.",
            "Maintain good soil drainage.",
            "Monitor for blight symptoms.",
            "Handle harvested tubers carefully."
        ]
    },


    "Soybean": {

        "overview":
            "Soybean is an important Kharif crop used as an oilseed and protein-rich crop. It performs well in suitable warm conditions and well-drained soil.",

        "season":
            "Generally grown during the Kharif season in many parts of India.",

        "sowing":
            "Use healthy seed and sow at the recommended time based on rainfall and local conditions. Avoid poorly drained fields.",

        "irrigation":
            "Soybean generally requires adequate moisture during important growth stages but is sensitive to prolonged waterlogging.",

        "fertilizer":
            "Nutrient management should be based on soil testing and local recommendations. Avoid unnecessary fertilizer application.",

        "nutrients":
            "Balanced phosphorus, potassium and other nutrients support root development, nodulation and crop growth.",

        "pests":
            "Stem flies, girdle beetles, defoliating insects and other pests may occur depending on region.",

        "diseases":
            "Rust, bacterial diseases and other fungal or viral diseases may occur under favourable conditions.",

        "prevention":
            "Use healthy seed, maintain proper spacing, monitor the crop regularly and maintain field sanitation.",

        "weeds":
            "Early weed management is very important because weeds compete strongly with soybean plants during establishment.",

        "harvesting":
            "Harvest when pods and plants reach appropriate maturity and excessive field losses can be avoided.",

        "storage":
            "Dry harvested soybean properly and store it in a clean, dry and pest-protected place.",

        "tips": [
            "Use quality seed.",
            "Avoid poorly drained fields.",
            "Maintain timely weed control.",
            "Monitor pests regularly.",
            "Dry grain properly before storage."
        ]
    }
}


# =========================================================
# DEFAULT ADVISORY FOR NEW CROPS
# =========================================================

DEFAULT_ADVISORY = {

    "overview":
        "This crop should be cultivated according to its local climate, soil condition, variety and recommended agricultural practices.",

    "season":
        "The suitable growing season depends on the crop variety, region and local climate.",

    "sowing":
        "Use healthy seed or planting material and follow the recommended sowing method, depth and spacing.",

    "irrigation":
        "Provide irrigation according to soil moisture, rainfall and crop growth stage. Avoid waterlogging.",

    "fertilizer":
        "Use soil-test-based fertilizer recommendations and maintain balanced nutrient management.",

    "nutrients":
        "Balanced plant nutrition supports healthy growth, development and crop quality.",

    "pests":
        "Pests may vary according to crop, season and location. Regular crop monitoring is recommended.",

    "diseases":
        "Diseases depend on environmental conditions, crop variety and field management.",

    "prevention":
        "Use healthy planting material, maintain field hygiene and monitor the crop regularly.",

    "weeds":
        "Timely weed management reduces competition for water, nutrients and sunlight.",

    "harvesting":
        "Harvest according to the recommended maturity stage for the selected crop and variety.",

    "storage":
        "Store harvested produce in a clean, dry and suitable storage environment.",

    "tips": [
        "Use quality planting material.",
        "Monitor soil moisture regularly.",
        "Follow soil-test-based nutrient management.",
        "Inspect the crop regularly.",
        "Follow local agricultural recommendations."
    ]
}


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# CROP ADVISORY
# =========================================================

@app.route("/crops")
def crops():

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed. Please check MySQL settings."

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type,
                created_at
            FROM crops
            ORDER BY id ASC
        """)

        crops_list = cursor.fetchall()

        return render_template(
            "crops.html",
            crops=crops_list,
            crop_icons=CROP_ICONS,
            crop_descriptions=CROP_DESCRIPTIONS
        )

    except Error as e:

        print("Crop Advisory Error:", e)

        return "Something went wrong while loading Crop Advisory."

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# CROP DETAILS
# =========================================================

@app.route("/crop-details/<crop_name>")
def crop_details(crop_name):

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type
            FROM crops
            WHERE LOWER(crop_name) = LOWER(%s)
            LIMIT 1
        """, (crop_name,))

        crop = cursor.fetchone()

        if crop is None:
            return "Crop not found", 404

        actual_crop_name = crop["crop_name"]

        data = {
            "type": crop["crop_type"],
            "temperature": crop["temperature"],
            "water": crop["water_requirement"],
            "soil": crop["soil_type"]
        }

        advisory = CROP_ADVISORY.get(
            actual_crop_name,
            DEFAULT_ADVISORY
        )

        icon = CROP_ICONS.get(
            actual_crop_name,
            "🌱"
        )

        return render_template(
            "crop_details.html",
            crop_name=actual_crop_name,
            data=data,
            advisory=advisory,
            icon=icon
        )

    except Error as e:

        print("Crop Details Error:", e)

        return "Something went wrong while loading crop details."

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# FERTILIZER ADVISORY
# =========================================================

@app.route("/fertilizer")
def fertilizer():

    return render_template("fertilizer.html")


# =========================================================
# DISEASE ADVISORY
# =========================================================

@app.route("/disease")
def disease():

    return render_template("disease.html")


# =========================================================
# GOVERNMENT SCHEMES
# =========================================================

@app.route("/schemes")
def schemes():

    return render_template("schemes.html")


# =========================================================
# AGRICULTURE POLICIES
# =========================================================

@app.route("/policies")
def policies():

    return render_template("policies.html")


# =========================================================
# AGRICULTURAL INSTITUTES
# =========================================================

@app.route("/institutes")
def institutes():

    return render_template("institutes.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""
    message_type = ""

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        connection = get_db_connection()

        if connection is None:

            message = "Database connection failed. Please check MySQL settings."
            message_type = "error"

            return render_template(
                "login.html",
                message=message,
                message_type=message_type
            )

        cursor = None

        try:

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    id,
                    full_name,
                    email,
                    user_type,
                    password
                FROM users
                WHERE email = %s
            """

            cursor.execute(query, (email,))

            user = cursor.fetchone()

            if user and check_password_hash(
                user["password"],
                password
            ):

                session["user_id"] = user["id"]
                session["full_name"] = user["full_name"]
                session["email"] = user["email"]
                session["user_type"] = user["user_type"]

                return redirect(url_for("home"))

            else:

                message = "Invalid email or password."
                message_type = "error"

        except Error as e:

            print("Login Error:", e)

            message = "Something went wrong while logging in."
            message_type = "error"

        finally:

            if cursor:
                cursor.close()

            connection.close()

    return render_template(
        "login.html",
        message=message,
        message_type=message_type
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""
    message_type = ""

    if request.method == "POST":

        full_name = request.form.get("name")
        email = request.form.get("email")
        user_type = request.form.get("role")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            message = "Passwords do not match."
            message_type = "error"

            return render_template(
                "register.html",
                message=message,
                message_type=message_type
            )

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        if connection is None:

            message = "Database connection failed. Please check MySQL settings."
            message_type = "error"

            return render_template(
                "register.html",
                message=message,
                message_type=message_type
            )

        cursor = None

        try:

            cursor = connection.cursor()

            check_query = """
                SELECT id
                FROM users
                WHERE email = %s
            """

            cursor.execute(
                check_query,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                message = "This email is already registered."
                message_type = "error"

            else:

                insert_query = """
                    INSERT INTO users
                    (
                        full_name,
                        email,
                        user_type,
                        password
                    )
                    VALUES (%s, %s, %s, %s)
                """

                cursor.execute(
                    insert_query,
                    (
                        full_name,
                        email,
                        user_type,
                        hashed_password
                    )
                )

                connection.commit()

                message = "Registration successful! You can now login."
                message_type = "success"

        except Error as e:

            print("Registration Error:", e)

            message = "Something went wrong during registration."
            message_type = "error"

        finally:

            if cursor:
                cursor.close()

            connection.close()

    return render_template(
        "register.html",
        message=message,
        message_type=message_type
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if not is_admin():
        return redirect(url_for("login"))

    search = request.args.get(
        "search",
        ""
    ).strip()

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        # -------------------------------------------------
        # USER COUNTS
        # -------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) AS total FROM users"
        )

        total_users = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM users
            WHERE LOWER(user_type) = 'farmer'
        """)

        farmers = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM users
            WHERE LOWER(user_type) = 'student'
        """)

        students = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM users
            WHERE LOWER(user_type) = 'admin'
        """)

        admins = cursor.fetchone()["total"]

        # -------------------------------------------------
        # USER SEARCH
        # -------------------------------------------------

        if search:

            user_query = """
                SELECT
                    id,
                    full_name,
                    email,
                    user_type,
                    created_at
                FROM users
                WHERE full_name LIKE %s
                   OR email LIKE %s
                   OR user_type LIKE %s
                ORDER BY id DESC
            """

            search_value = "%" + search + "%"

            cursor.execute(
                user_query,
                (
                    search_value,
                    search_value,
                    search_value
                )
            )

        else:

            cursor.execute("""
                SELECT
                    id,
                    full_name,
                    email,
                    user_type,
                    created_at
                FROM users
                ORDER BY id DESC
            """)

        users = cursor.fetchall()

        # -------------------------------------------------
        # CROP DATA
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type,
                created_at
            FROM crops
            ORDER BY id DESC
        """)

        crops_list = cursor.fetchall()

        return render_template(
            "admin.html",
            total_users=total_users,
            farmers=farmers,
            students=students,
            admins=admins,
            users=users,
            crops=crops_list,
            search=search
        )

    except Error as e:

        print("Admin Dashboard Error:", e)

        return "Something went wrong while loading Admin Dashboard."

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# DELETE USER
# =========================================================

@app.route(
    "/admin/delete-user/<int:user_id>",
    methods=["POST"]
)
def delete_user(user_id):

    if not is_admin():
        return redirect(url_for("login"))

    # Prevent admin from deleting own account
    if user_id == session.get("user_id"):
        return redirect(url_for("admin"))

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

        connection.commit()

    except Error as e:

        print("Delete User Error:", e)

    finally:

        if cursor:
            cursor.close()

        connection.close()

    return redirect(url_for("admin"))


# =========================================================
# ADD CROP
# =========================================================

@app.route(
    "/admin/add-crop",
    methods=["POST"]
)
def add_crop():

    if not is_admin():
        return redirect(url_for("login"))

    crop_name = request.form.get(
        "crop_name",
        ""
    ).strip()

    crop_type = request.form.get(
        "crop_type",
        ""
    ).strip()

    temperature = request.form.get(
        "temperature",
        ""
    ).strip()

    water_requirement = request.form.get(
        "water_requirement",
        ""
    ).strip()

    soil_type = request.form.get(
        "soil_type",
        ""
    ).strip()

    if not crop_name:
        return redirect(url_for("admin"))

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:

        cursor = connection.cursor()

        query = """
            INSERT INTO crops
            (
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type
            )
        )

        connection.commit()

    except Error as e:

        print("Add Crop Error:", e)

    finally:

        if cursor:
            cursor.close()

        connection.close()

    return redirect(url_for("admin"))


# =========================================================
# EDIT CROP
# =========================================================

@app.route(
    "/admin/edit-crop/<int:crop_id>",
    methods=["GET", "POST"]
)
def edit_crop(crop_id):

    if not is_admin():
        return redirect(url_for("login"))

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:

        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            crop_name = request.form.get(
                "crop_name",
                ""
            ).strip()

            crop_type = request.form.get(
                "crop_type",
                ""
            ).strip()

            temperature = request.form.get(
                "temperature",
                ""
            ).strip()

            water_requirement = request.form.get(
                "water_requirement",
                ""
            ).strip()

            soil_type = request.form.get(
                "soil_type",
                ""
            ).strip()

            update_query = """
                UPDATE crops
                SET
                    crop_name = %s,
                    crop_type = %s,
                    temperature = %s,
                    water_requirement = %s,
                    soil_type = %s
                WHERE id = %s
            """

            cursor.execute(
                update_query,
                (
                    crop_name,
                    crop_type,
                    temperature,
                    water_requirement,
                    soil_type,
                    crop_id
                )
            )

            connection.commit()

            return redirect(url_for("admin"))

        cursor.execute(
            """
            SELECT
                id,
                crop_name,
                crop_type,
                temperature,
                water_requirement,
                soil_type
            FROM crops
            WHERE id = %s
            """,
            (crop_id,)
        )

        crop = cursor.fetchone()

        if crop is None:
            return "Crop not found.", 404

        return render_template(
            "edit_crop.html",
            crop=crop
        )

    except Error as e:

        print("Edit Crop Error:", e)

        return "Something went wrong while editing crop."

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# DELETE CROP
# =========================================================

@app.route(
    "/admin/delete-crop/<int:crop_id>",
    methods=["POST"]
)
def delete_crop(crop_id):

    if not is_admin():
        return redirect(url_for("login"))

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM crops WHERE id = %s",
            (crop_id,)
        )

        connection.commit()

    except Error as e:

        print("Delete Crop Error:", e)

    finally:

        if cursor:
            cursor.close()

        connection.close()

    return redirect(url_for("admin"))


# =========================================================
# RUN FLASK SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5050")),
        debug=False
    )
