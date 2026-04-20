(function () {
  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  const navLinks = Array.from(document.querySelectorAll(".site-nav a"));
  const sections = Array.from(document.querySelectorAll("main section[id]"));
  const revealNodes = Array.from(document.querySelectorAll(".reveal"));
  const footerYear = document.querySelector("[data-year]");

  if (footerYear) {
    footerYear.textContent = String(new Date().getFullYear());
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      const isOpen = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Highlight the active section in the navbar.
  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    const linkById = new Map(
      navLinks
        .map(function (link) {
          const hash = link.getAttribute("href") || "";
          return [hash.replace("#", ""), link];
        })
        .filter(function (entry) {
          return Boolean(entry[0]);
        })
    );

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }

          const id = entry.target.getAttribute("id");
          const activeLink = id ? linkById.get(id) : null;
          if (!activeLink) {
            return;
          }

          navLinks.forEach(function (link) {
            link.classList.remove("is-active");
          });
          activeLink.classList.add("is-active");
        });
      },
      {
        rootMargin: "-35% 0px -55% 0px",
        threshold: 0.1,
      }
    );

    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  // Staggered reveal animation on first scroll into view.
  if (revealNodes.length && "IntersectionObserver" in window) {
    revealNodes.forEach(function (node, index) {
      node.style.transitionDelay = (index % 6) * 70 + "ms";
    });

    const revealObserver = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        });
      },
      {
        threshold: 0.16,
        rootMargin: "0px 0px -40px 0px",
      }
    );

    revealNodes.forEach(function (node) {
      revealObserver.observe(node);
    });
  } else {
    revealNodes.forEach(function (node) {
      node.classList.add("is-visible");
    });
  }
})();
