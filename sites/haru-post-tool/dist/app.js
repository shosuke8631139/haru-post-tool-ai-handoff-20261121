function withCb(url) { return url ? `${url}?v=20261124greatlife` : url; }
const app = document.querySelector('#app');
const toast = document.querySelector('#toast');

function escapeHtml(value = '') {
  return value.replace(/[&<>'"]/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[char]);
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => toast.classList.remove('show'), 1800);
}

async function copyText(value) {
  try {
    await navigator.clipboard.writeText(value);
    showToast('コピーしました');
  } catch {
    const area = document.createElement('textarea');
    area.value = value;
    document.body.appendChild(area);
    area.select();
    document.execCommand('copy');
    area.remove();
    showToast('コピーしました');
  }
}

function safeFilename(value = '投稿画像') {
  return value.replace(/[\\/:*?"<>|]/g, '').trim() || '投稿画像';
}

async function getMediaFile(src, label, kind) {
  const response = await fetch(src, { cache: 'no-store' });
  if (!response.ok) throw new Error('media fetch failed');
  const blob = await response.blob();
  const extension = kind === 'video' ? 'mp4' : (blob.type.includes('jpeg') ? 'jpg' : 'png');
  const mime = blob.type || (kind === 'video' ? 'video/mp4' : 'image/png');
  return { blob, file: new File([blob], `${safeFilename(label)}.${extension}`, { type: mime }) };
}

function downloadBlob(blob, filename) {
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = objectUrl;
  link.download = filename;
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
}

async function saveMedia(src, label, button, kind) {
  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = `${kind === 'video' ? '動画' : '画像'}を準備中…`;

  try {
    const { blob, file } = await getMediaFile(src, label, kind);
    downloadBlob(blob, file.name);
    showToast(`${kind === 'video' ? '動画' : '画像'}を保存しました`);
  } catch (error) {
    showToast('保存できませんでした。共有ボタンをお試しください');
  } finally {
    button.disabled = false;
    button.textContent = originalText;
  }
}

async function shareMedia(src, label, button, kind) {
  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = '共有を準備中…';
  try {
    const { file } = await getMediaFile(src, label, kind);
    if (!navigator.share || !navigator.canShare?.({ files: [file] })) {
      showToast('この端末では共有できません。保存ボタンをご利用ください');
      return;
    }
    await navigator.share({ files: [file], title: label });
    showToast('共有しました');
  } catch (error) {
    showToast(error?.name === 'AbortError' ? '共有を閉じました' : '共有できませんでした');
  } finally {
    button.disabled = false;
    button.textContent = originalText;
  }
}

function postPanel(id, title, text, buttonClass = '') {
  return `
    <section class="panel" id="${id}">
      <div class="panel__head">
        <h3>${title}<span class="counter">${[...text].length}文字</span></h3>
        <button class="copy-button ${buttonClass}" data-copy="${id}">コピー</button>
      </div>
      <pre class="post-text ${id !== 'long' ? 'post-text--short' : ''}" data-text="${id}">${escapeHtml(text)}</pre>
    </section>`;
}

function renderSelector(items, selectedId) {
  return `
    <section class="library-card" aria-labelledby="library-title">
      <label id="library-title" for="post-selector">過去の投稿セットから選ぶ</label>
      <div class="select-wrap">
        <select id="post-selector">
          ${items.map((item, index) => `
            <option value="${escapeHtml(item.id)}" ${item.id === selectedId ? 'selected' : ''}>
              ${index === 0 ? '最新｜' : ''}${escapeHtml(item.title)}
            </option>`).join('')}
        </select>
      </div>
      <p>選ぶと、投稿文・ハッシュタグ・画像がまとめて切り替わります。</p>
    </section>`;
}

function renderPost(data, allItems) {
  const videos = data.videos?.length ? data.videos : (data.video ? [data.video] : []);
  const videoNav = videos.length ? '<a href="#short-video">動画</a>' : '';
  const videoPanel = videos.length ? `
    <section class="panel" id="short-video">
      <div class="panel__head">
        <h3>ショート動画<span class="counter">${videos.length}本</span></h3>
      </div>
      <div class="video-grid">
        ${videos.map((video) => `
          <div class="video-card">
            <video controls playsinline muted preload="metadata" poster="${withCb(video.poster)}">
              <source src="${withCb(video.src)}" type="video/mp4" />
              このブラウザでは動画を再生できません。
            </video>
            <div class="video-card__body">
              <strong>${escapeHtml(video.label)}</strong>
              <p>縦型9:16・日本語ナレーション付き・${escapeHtml(video.duration)}</p>
              <div class="media-actions">
                <button class="download-button" type="button" data-save-media="${video.src}" data-media-label="${escapeHtml(video.label)}" data-media-kind="video">動画を保存</button>
                <button class="share-button" type="button" data-share-media="${video.src}" data-media-label="${escapeHtml(video.label)}" data-media-kind="video">共有</button>
              </div>
            </div>
          </div>`).join('')}
      </div>
    </section>` : '';

  app.innerHTML = `
    ${renderSelector(allItems, data.id)}

    <section class="topic-card">
      <div class="meta">作成：${escapeHtml(data.updatedAt)}</div>
      <h2>${escapeHtml(data.title)}</h2>
      <div class="meta">${escapeHtml(data.sourceTitle)}</div>
      <a class="source-link" href="${data.sourceUrl}" target="_blank" rel="noopener">YouTubeの参考動画を開く</a>
    </section>

    <nav class="quick-nav" aria-label="ページ内メニュー">
      <a href="#long">長文</a><a href="#medium">500文字</a><a href="#x-post">X投稿</a><a href="#images">画像</a>${videoNav}
    </nav>

    ${postPanel('long', '長文投稿', data.longPost)}
    ${postPanel('medium', '約500文字投稿', data.mediumPost, 'copy-button--teal')}
    ${postPanel('x-post', 'X用投稿', data.xPost, 'copy-button--orange')}
    ${postPanel('hashtags', 'ハッシュタグ候補', data.hashtags)}

    <section class="panel" id="images">
      <div class="panel__head"><h3>投稿画像</h3></div>
      <div class="image-grid">
        ${data.images.map((image) => `
          <article class="image-card">
            <img src="${withCb(image.src)}" alt="${escapeHtml(image.label)}" loading="lazy" />
            <div class="image-card__body">
              <h4>${escapeHtml(image.label)}</h4>
              <div class="media-actions">
                <button class="download-button" type="button" data-save-media="${image.src}" data-media-label="${escapeHtml(image.label)}" data-media-kind="image">画像を保存</button>
                <button class="share-button" type="button" data-share-media="${image.src}" data-media-label="${escapeHtml(image.label)}" data-media-kind="image">共有</button>
              </div>
            </div>
          </article>`).join('')}
      </div>
    </section>

    ${videoPanel}

    <aside class="home-tip">
      <strong>ホーム画面に置く方法</strong><br />
      iPhoneはSafariの共有ボタンから「ホーム画面に追加」。AndroidはChromeのメニューから「ホーム画面に追加」を選びます。
    </aside>`;

  document.querySelector('#post-selector').addEventListener('change', (event) => {
    const next = allItems.find((item) => item.id === event.target.value);
    if (!next) return;
    localStorage.setItem('haru-selected-post', next.id);
    renderPost(next, allItems);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', () => {
      const key = button.dataset.copy;
      const text = document.querySelector(`[data-text="${key}"]`).textContent;
      copyText(text);
    });
  });

  document.querySelectorAll('[data-save-media]').forEach((button) => {
    button.addEventListener('click', () => {
      saveMedia(button.dataset.saveMedia, button.dataset.mediaLabel, button, button.dataset.mediaKind);
    });
  });

  document.querySelectorAll('[data-share-media]').forEach((button) => {
    button.addEventListener('click', () => {
      shareMedia(button.dataset.shareMedia, button.dataset.mediaLabel, button, button.dataset.mediaKind);
    });
  });
}

async function init() {
  const response = await fetch('content.json?v=20261124psychology', { cache: 'no-store' });
  if (!response.ok) throw new Error('content.json could not be loaded');
  const data = await response.json();
  const items = data.items || [data];
  const remembered = localStorage.getItem('haru-selected-post');
  const selected = items.find((item) => item.id === remembered)
    || items.find((item) => item.id === data.latest)
    || items[0];
  renderPost(selected, items);
}

init().catch(() => {
  app.innerHTML = '<section class="panel"><h3>読み込みに失敗しました</h3><p>時間を置いて、もう一度ページを開いてください。</p></section>';
});
