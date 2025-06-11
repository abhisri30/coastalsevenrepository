import React, { useEffect, useRef } from 'react';
import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js';

const Globe = () => {
  const mountRef = useRef(null);
  const rendererRef = useRef(null);

  useEffect(() => {
    if (!mountRef.current) return;

    try {
      // Scene setup
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        75,
        mountRef.current.clientWidth / mountRef.current.clientHeight,
        0.1,
        1000
      );
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setClearColor(0x000000, 0); // Transparent background
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
      mountRef.current.appendChild(renderer.domElement);
      rendererRef.current = renderer;

      // Globe
      const geometry = new THREE.SphereGeometry(5, 32, 32);
      const textureLoader = new THREE.TextureLoader();
      const texture = textureLoader.load(
        'https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg',
        () => console.log('Texture loaded successfully'),
        undefined,
        (err) => console.error('Texture loading failed:', err)
      );
      const material = new THREE.MeshPhongMaterial({
        map: texture,
        color: texture ? 0xffffff : 0x0000ff // Fallback to blue if texture fails
      });
      const globe = new THREE.Mesh(geometry, material);
      scene.add(globe);

      // Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);
      const pointLight = new THREE.PointLight(0xffffff, 0.5);
      pointLight.position.set(10, 10, 10);
      scene.add(pointLight);

      camera.position.z = 15;

      // Animation
      let animationFrameId;
      const animate = () => {
        animationFrameId = requestAnimationFrame(animate);
        globe.rotation.y += 0.005;
        renderer.render(scene, camera);
      };
      animate();

      // Handle resize
      const handleResize = () => {
        if (mountRef.current) {
          camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        }
      };
      window.addEventListener('resize', handleResize);

      // Cleanup
      return () => {
        window.removeEventListener('resize', handleResize);
        cancelAnimationFrame(animationFrameId);
        if (mountRef.current && renderer.domElement) {
          mountRef.current.removeChild(renderer.domElement);
        }
        renderer.dispose();
      };
    } catch (error) {
      console.error('Error setting up Three.js:', error);
    }
  }, []);

  return (
    <div
      ref={mountRef}
      style={{
        width: '100%',
        height: '100vh',
        backgroundColor: '#111827', // Dark gray background
        position: 'relative',
        overflow: 'hidden'
      }}
    />
  );
};

export default Globe;