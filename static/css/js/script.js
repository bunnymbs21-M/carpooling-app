document.addEventListener('DOMContentLoaded', () => {
    // --- Scroll Reveal Animation ---
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                
                // If it's the stats section, start the number counter
                if(entry.target.classList.contains('stats-section')) {
                    startCounters();
                }
            }
        });
    }, observerOptions);

    // Grab all elements with the 'hidden' class and observe them
    const hiddenElements = document.querySelectorAll('.hidden');
    hiddenElements.forEach((el) => observer.observe(el));

    // --- Number Counter Animation ---
    let counted = false;
    
    function startCounters() {
        if(counted) return;
        counted = true;

        const counters = document.querySelectorAll('.counter');
        const speed = 200; 

        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 20);
                } else {
                    counter.innerText = target + "+";
                }
            };
            updateCount();
        });
    }
});
