
import streamlit as st
import streamlit.components.v1 as components

def render_3d_mineral(mineral_name, height=350):
    """
    Render an interactive 3D mineral viewer with orbit controls.
    The mineral shape and colour are based on the identified mineral.
    """
    # Colour map (approximate real mineral colours)
    mineral_colors = {
        "Biotite": 0x3e2723,       # dark brown
        "Bornite": 0x8a2be2,       # purple/blue iridescent
        "Chrysocolla": 0x00bcd4,   # cyan-blue
        "Malachite": 0x00c853,     # green
        "Muscovite": 0xe0e0e0,     # silver/white
        "Pyrite": 0xffd700,        # gold
        "Quartz": 0xf5f5f5,        # white/clear
    }
    color = mineral_colors.get(mineral_name, 0xcccccc)

    # Shape mapping: pyrite = cube, quartz = hexagonal prism, others = octahedron
    shape = "cube" if mineral_name == "Pyrite" else "octahedron"
    if mineral_name == "Quartz":
        shape = "hexagonal"

    # Build geometry and wireframe in JavaScript based on shape
    shape_js = ""
    if shape == "cube":
        shape_js = "new THREE.BoxGeometry(1.5, 1.5, 1.5)"
    elif shape == "hexagonal":
        shape_js = "new THREE.CylinderGeometry(1.0, 1.0, 2.0, 6)"  # hexagonal prism
    else:
        shape_js = "new THREE.OctahedronGeometry(1.2, 0)"

    # Three.js + OrbitControls from CDN
    three_js = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
    orbit_js = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="{three_js}"></script>
        <script src="{orbit_js}"></script>
    </head>
    <body style="margin:0; display:flex; justify-content:center; align-items:center; background:transparent;">
        <div id="container" style="width:100%; height:{height}px; cursor:grab;"></div>
        <script>
            const container = document.getElementById('container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 4;

            const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setClearColor(0x000000, 0);
            container.appendChild(renderer.domElement);

            // Controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 2.0;
            controls.enableZoom = true;

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight1.position.set(5, 10, 7);
            scene.add(dirLight1);
            const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
            dirLight2.position.set(-5, -3, -5);
            scene.add(dirLight2);

            // Mineral mesh
            const geometry = {shape_js};
            const material = new THREE.MeshStandardMaterial({{
                color: {color},
                roughness: 0.25,
                metalness: 0.75,
                transparent: true,
                opacity: 0.85
            }});
            const mineral = new THREE.Mesh(geometry, material);
            scene.add(mineral);

            // Wireframe edges
            const edges = new THREE.EdgesGeometry(geometry);
            const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({{ color: 0xffffff, linewidth: 1 }}));
            mineral.add(line);

            // Particle sparkle
            const particlesGeo = new THREE.BufferGeometry();
            const particleCount = 100;
            const positions = new Float32Array(particleCount * 3);
            for (let i = 0; i < particleCount * 3; i += 3) {{
                positions[i] = (Math.random() - 0.5) * 4;
                positions[i+1] = (Math.random() - 0.5) * 4;
                positions[i+2] = (Math.random() - 0.5) * 4;
            }}
            particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const particlesMat = new THREE.PointsMaterial({{
                size: 0.02,
                color: 0xffffff,
                transparent: true,
                opacity: 0.6
            }});
            const particles = new THREE.Points(particlesGeo, particlesMat);
            scene.add(particles);

            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                controls.update(); // handles autoRotate and damping
                particles.rotation.y += 0.0005;
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html, height=height+20)
