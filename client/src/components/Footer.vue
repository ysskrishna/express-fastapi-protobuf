<template>
  <footer class="footer">
    <div class="footer-left">
      <a
        class="profile"
        href="https://github.com/ysskrishna"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img class="avatar" src="https://github.com/ysskrishna.png" alt="Y. Siva Sai Krishna" />
        <div class="profile-text">
          <div class="name">Y. Siva Sai Krishna</div>
          <div class="handle">@ysskrishna</div>
        </div>
      </a>
    </div>

    <div class="footer-right">
      <a
        class="btn view-project"
        href="https://github.com/ysskrishna/express-fastapi-protobuf"
        target="_blank"
        rel="noopener noreferrer"
      >
        View Project
      </a>

      <nav class="socials" aria-label="social links">
        <a href="https://github.com/ysskrishna" target="_blank" rel="noopener noreferrer" class="icon-link" aria-label="GitHub">
          <IconFaBrandsGithub class="icon" />
        </a>

        <a href="https://linkedin.com/in/ysskrishna" target="_blank" rel="noopener noreferrer" class="icon-link" aria-label="LinkedIn">
          <IconFaBrandsLinkedin class="icon" />
        </a>

        <a href="https://www.youtube.com/@ysskrishna" target="_blank" rel="noopener noreferrer" class="icon-link" aria-label="YouTube">
          <IconFaBrandsYoutube class="icon" />
        </a>

        <a href="https://www.producthunt.com/@ysskrishna" target="_blank" rel="noopener noreferrer" class="icon-link" aria-label="Product Hunt">
          <IconSimpleProductHunt class="icon" />
        </a>
      </nav>
    </div>
  </footer>
</template>

<script setup>
import IconFaBrandsGithub from '~icons/fa-brands/github';
import IconFaBrandsLinkedin from '~icons/fa-brands/linkedin';
import IconFaBrandsYoutube from '~icons/fa-brands/youtube';
import IconSimpleProductHunt from '~icons/simple-icons/producthunt';

const props = defineProps({
  authenticated: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 0;
  margin-top: 22px;
  border-top: 1px solid rgba(0,0,0,0.06);
}
.footer-left { display:flex; align-items:center; }
.profile { display:flex; align-items:center; gap:12px; text-decoration:none; color:inherit; }
.avatar { width:40px; height:40px; border-radius:50%; object-fit:cover; }
.profile-text .name { font-weight:600; }
.profile-text .handle { font-size:0.85rem; color:var(--muted, #6b7280); }

.footer-right { display:flex; align-items:center; gap:12px; }
.btn.view-project {
  display:inline-block;
  padding:8px 12px;
  border-radius:8px;
  border:1px solid rgba(0,0,0,0.08);
  background:transparent;
  text-decoration:none;
  color:inherit;
  font-weight:600;
}
.socials { display:flex; gap:10px; align-items:center; }
.icon-link { color:var(--muted, #6b7280); display:inline-flex; align-items:center; }
.icon-link svg { display:block; }
.icon { width:20px; height:20px; display:inline-block; color:inherit; }
.icon svg { width:100%; height:100%; display:block; }

@media (max-width:640px) {
  .footer { padding:12px 0; }
  .footer-right { width:100%; justify-content:flex-start; }
}
</style>

