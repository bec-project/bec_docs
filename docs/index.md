---
hide:
  - navigation
  - toc
---

<section class="bec-home">
  <div class="bec-home__hero">
    <div class="bec-home__intro">
      <p class="bec-home__eyebrow">Beamline Experiment Control</p>
      <h1>BEC</h1>
      <p class="bec-home__lead">
        A modular platform for data acquisition, device control, and scan orchestration at large research facilities.
      </p>
      <div class="bec-home__actions">
        <a class="md-button md-button--primary" href="getting-started/">Get started</a>
        <a class="md-button" href="developer/getting_started/architecture.html">See architecture</a>
      </div>
      <div class="bec-home__meta">
        <div>
          <strong>Users</strong>
          <span>CLI, GUI, scans, and live data workflows</span>
        </div>
        <div>
          <strong>Operators</strong>
          <span>Service layout, deployment, and configuration</span>
        </div>
        <div>
          <strong>Developers</strong>
          <span>Devices, plugins, scans, and APIs</span>
        </div>
      </div>
    </div>

    <div class="bec-home__visual">
      <div class="bec-home__frame">
        <img src="assets/BEC_context_user_centric.png" alt="BEC system overview" />
      </div>
      <div class="bec-home__badge bec-home__badge--one">Scans</div>
      <div class="bec-home__badge bec-home__badge--two">Devices</div>
      <div class="bec-home__badge bec-home__badge--three">Data</div>
    </div>
  </div>

  <div class="bec-home__strip">
    <article>
      <span>01</span>
      <h2>Queue-driven orchestration</h2>
      <p>Coordinate scans, device actions, and data collection without coupling users to backend services.</p>
    </article>
    <article>
      <span>02</span>
      <h2>Built for beamline workflows</h2>
      <p>Move from interactive control to automated pipelines with the same shared system model.</p>
    </article>
    <article>
      <span>03</span>
      <h2>Modular by design</h2>
      <p>Extend the platform through Ophyd devices, scan plugins, UI tooling, and service integrations.</p>
    </article>
  </div>

  <section class="bec-home__section">
    <div class="bec-home__section-head">
      <p>Choose your entry point</p>
      <h2>Start with the part of BEC you need today.</h2>
    </div>

    <div class="bec-home__cards">
      <a class="bec-card" href="user/user.html">
        <div class="bec-card__label">User Guide</div>
        <h3>Operate BEC from the CLI and GUI</h3>
        <p>Install the client, load devices, run scans, and inspect live data and plots.</p>
      </a>

      <a class="bec-card" href="developer/developer.html">
        <div class="bec-card__label">Developer Guide</div>
        <h3>Extend devices, scans, and interfaces</h3>
        <p>Set up a development environment and work across plugins, device layers, and scan logic.</p>
      </a>

      <a class="bec-card" href="developer/getting_started/architecture.html">
        <div class="bec-card__label">Architecture</div>
        <h3>Understand how the services fit together</h3>
        <p>Follow the flow between Redis, scan orchestration, file writing, synchronization, and clients.</p>
      </a>

      <a class="bec-card" href="api_reference/api_reference.html">
        <div class="bec-card__label">Reference</div>
        <h3>Browse technical details and API entry points</h3>
        <p>Use the translated reference pages as a Material-based prototype for deeper system details.</p>
      </a>
    </div>
  </section>

  <section class="bec-home__section bec-home__section--alt">
    <div class="bec-home__section-head">
      <p>Core areas</p>
      <h2>The main parts of the documentation.</h2>
    </div>

    <div class="bec-home__panels">
      <a class="bec-panel" href="developer/devices/devices.html">
        <h3>Devices</h3>
        <p>Ophyd integration, configuration, simulation, and external data sources.</p>
      </a>
      <a class="bec-panel" href="developer/scans/scans.html">
        <h3>Scans</h3>
        <p>Scan structure, metadata, stubs, GUI configuration, and plugin tutorials.</p>
      </a>
      <a class="bec-panel" href="developer/data_access/data_access.html">
        <h3>Data access</h3>
        <p>Messaging, event streams, synchronized readouts, and file-writer behavior.</p>
      </a>
      <a class="bec-panel" href="developer/user_interfaces/user_interfaces.html">
        <h3>User interfaces</h3>
        <p>Command-line workflows, GUI usage, and client-side extension points.</p>
      </a>
    </div>
  </section>
</section>
