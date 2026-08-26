
import streamlit as st
import streamlit.components.v1 as components

def render_3d_mineral(mineral_name, height=300):
    """
    Render an interactive 3D mineral viewer using Three.js.
    The mineral is shown as a rotating crystal with a representative color.
    """
    # Map mineral to color (approximate) and shape type
    mineral_colors = {
        "Biotite": 0x3e2723,   # dark brown
        "Bornite": 0x7b2ff7,   # purple/blue iridescent
        "Chrysocolla": 0x00bcd4, # cyan-blue
        "Malachite": 0x00c853,  # green
        "Muscovite": 0xe0e0e0,  # silver/white
        "Pyrite": 0xffd700,     # gold
        "Quartz": 0xf5f5f5,     # white/clear
    }
    color = mineral_colors.get(mineral_name, 0xcccccc)
    
    # Shape type: we can vary geometry per mineral, but for simplicity use a crystal-like octahedron
    # Pyrite often forms cubes, so we can use a cube for pyrite.
    shape = "cube" if mineral_name == "Pyrite" else "octahedron"
    
    # Three.js CDN
    three_js = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="{three_js}"></script>
    </head>
    <body style="margin:0; display:flex; justify-content:center; align-items:center; background: transparent;">
        <div id="container" style="width:100%; height:{height}px; cursor:grab;"></div>
        <script>
            const container = document.getElementById('container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 4;
            
            const renderer = new THREE.WebGLRenderer({{ alpha: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setClearColor(0x000000, 0); // transparent background
            container.appendChild(renderer.domElement);
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 10, 7);
            scene.add(directionalLight);
            
            // Create mineral mesh
            let geometry;
            if ("{shape}" === "cube") {{
                geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
            }} else {{
                geometry = new THREE.OctahedronGeometry(1.2, 0);
            }}
            const material = new THREE.MeshStandardMaterial({{
                color: {color},
                roughness: 0.3,
                metalness: 0.7,
                transparent: true,
                opacity: 0.9
            }});
            const mineral = new THREE.Mesh(geometry, material);
            scene.add(mineral);
            
            // Add wireframe edges for more detail
            const edges = new THREE.EdgesGeometry(geometry);
            const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({{ color: 0xffffff, linewidth: 1 }}));
            mineral.add(line);
            
            // Rotation animation
            function animate() {{
                requestAnimationFrame(animate);
                mineral.rotation.x += 0.005;
                mineral.rotation.y += 0.01;
                renderer.render(scene, camera);
            }}
            animate();
            
            // Handle window resize
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
