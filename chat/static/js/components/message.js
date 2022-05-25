function boldExtension(name) {
    const frags = name.split(".");

    const extension = frags.pop();
    const filename = frags.join(".");

    return `
        <span>${filename}
            <b class='uk-text-warning uk-text-bold'>
                .${extension}
            </b>
        </span>
    `;
}

function createAttachments(attachments) {
    if (attachments || attachments.length === 0) return "";

    let block = "";

    for (let attachment in attachments) {
        block += `
            <li>
                <a target="_blank" class="link" href="${ attachment.file.url }">
                    ${boldExtension(attachment.file.name)}
                    <span>(${ attachment.file.size })</span>
                </a>
            </li>`
    }

    return block;
}

function createMessage(data) {
    return `
    <article class="uk-alert uk-comment uk-position-relative uk-padding-small uk-margin-small uk-border-rounded
            message ${data.author.id === me ? 'message-me uk-alert-success' : 'uk-alert-primary'}
            uk-box-shadow-hover-medium uk-text-secondary">

        <header class="uk-comment-header">
            <div class="uk-grid-medium uk-flex-middle" uk-grid>
                <div class="uk-width-auto">
                    <img class="uk-comment-avatar" src="${data.author.avatar_url}" width="42" height="42" alt="">
                </div>
                <div class="uk-width-expand">
                    <h4 class="uk-comment-title uk-margin-remove">
                        <a class="uk-link-reset" target="_blank"
                           href="${data.author.url}">${data.author.name}</a>
                    </h4>

                    <div class="uk-overflow-auto">
                        <ul class="uk-comment-meta uk-subnav-divider uk-subnav uk-margin-remove-top">
                            ${createAttachments(data.attachments)}
                        </ul>
                    </div>

                </div>
            </div>
        </header>

        <div class="uk-comment-body">
            <p>${decipher({box: data.content, nonce: data.nonce}, data.author.id)}</p>
        </div>
    </article>`;
}
