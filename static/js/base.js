document.addEventListener("DOMContentLoaded", () => {
  const groups = document.querySelectorAll("[data-collapsible]");
  const menuLinks = document.querySelectorAll(".menu-items a[href]");

  const clearActiveState = () => {
    document.querySelectorAll(".menu-items li.is-active-link").forEach((item) => {
      item.classList.remove("is-active-link");
    });
    document.querySelectorAll(".menu-items a.is-active").forEach((link) => {
      link.classList.remove("is-active");
      link.removeAttribute("aria-current");
    });
  };

  const setActiveLink = (link) => {
    clearActiveState();
    link.classList.add("is-active");
    link.setAttribute("aria-current", "page");

    const item = link.closest("li");
    if (item) {
      item.classList.add("is-active-link");
    }

    const group = link.closest(".menu-group");
    if (group) {
      group.classList.add("is-open");
    }
  };

  groups.forEach((group) => {
    const title = group.querySelector(".menu-title");
    if (!title) {
      return;
    }

    title.addEventListener("click", () => {
      group.classList.toggle("is-open");
    });
  });

  const currentPath = window.location.pathname.replace(/\/+$/, "") || "/";

  menuLinks.forEach((link) => {
    link.addEventListener("click", () => {
      setActiveLink(link);
    });

    const linkUrl = new URL(link.href, window.location.origin);
    const linkPath = linkUrl.pathname.replace(/\/+$/, "") || "/";
    const isExactMatch = linkPath === currentPath;
    const isChildMatch = linkPath !== "/" && currentPath.startsWith(`${linkPath}/`);

    if (!isExactMatch && !isChildMatch) {
      return;
    }

    setActiveLink(link);
  });
});
