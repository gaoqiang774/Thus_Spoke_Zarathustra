document.addEventListener('DOMContentLoaded', () => {
    
    // Intersection Observer for graceful scroll fade-ups
    const reveals = document.querySelectorAll('.reveal');
    
    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };
    
    const revealOnScroll = new IntersectionObserver(function(
        entries,
        observer
    ) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);
    
    reveals.forEach(reveal => {
        revealOnScroll.observe(reveal);
    });

    // Optional: Subtle parallax effect for hero if background-attachment: fixed is not enough
    const heroBg = document.querySelector('.hero-bg');
    
    window.addEventListener('scroll', () => {
        let scrollPosition = window.pageYOffset;
        if(heroBg && scrollPosition < window.innerHeight) {
            heroBg.style.transform = `translateY(${scrollPosition * 0.4}px) scale(1.05)`;
        }
    });

});
