import React from 'react';
import './Header.css';

const Header = () => {
  const scrollToSection = () => {
    const element = document.getElementById('explore-menu');
    if (element) {
      setTimeout(() => {
        element.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  return (
    <div className='header'>
      <div className="header-contents">
        <h2>Savor the Flavor, Delivered to Your Door!</h2>
        <p>Craving something delicious? Dive into our mouth-watering menu and treat yourself to the best food in town. From savory to sweet, we've got it all. Fresh ingredients, bold flavors, and speedy delivery—your perfect meal is just a click away!</p>
        <button onClick={scrollToSection}>View Menu</button>
      </div>
    </div>
  );
}

export default Header;
