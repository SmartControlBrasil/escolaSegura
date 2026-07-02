from django.test import TestCase
from apps.policy_guard.models import PrivacyConsentLog


class PublicSiteTests(TestCase):
    def test_main_routes_smoke_200(self):
        routes = [
            '/',
            '/home-two/',
            '/home-three/',
            '/about/',
            '/about-two/',
            '/instructor/',
            '/instructor-two/',
            '/instructor-details/',
            '/event/',
            '/event-single/',
            '/courses/',
            '/courses-sidebar/',
            '/single-course/',
            '/blog-standard/',
            '/single-blog/',
            '/contacts/',
            '/error/',
            '/sobre/',
            '/solucoes/',
            '/solucoes/controle-de-acesso-escolar/',
            '/solucoes/catraca-eletronica/',
            '/solucoes/cameras-de-monitoramento/',
            '/solucoes/cantina-pagamentos/',
            '/blog/',
            '/contato/',
            '/login/',
            '/recursos/',
            '/modulos/',
            '/planos/',
            '/faq/',
            '/demonstracao/',
            '/privacidade/',
            '/termos/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f'Route {route} failed with status {response.status_code}')

    def test_home_page_contains_edumim_menu_structure(self):
        response = self.client.get('/')
        self.assertContains(response, 'Home One')
        self.assertContains(response, 'Home Two')
        self.assertContains(response, 'Home Three')
        self.assertContains(response, 'Start Free Trial')
        self.assertContains(response, 'Blog Standard')
        self.assertContains(response, 'Single Blog')
        self.assertContains(response, 'Contacts')

    def test_home_page_contains_app_and_family_links(self):
        response = self.client.get('/')
        self.assertContains(response, '/app/')
        self.assertContains(response, '/familia/')

    def test_home_page_does_not_contain_old_branding(self):
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        self.assertNotIn('Intereal', content)
        self.assertNotIn('Marmoraria', content)
        self.assertNotIn('Santander', content)
        self.assertNotIn('Marble', content)
        self.assertNotIn('Interior Design', content)
        self.assertNotIn('Get A Quote', content)

    def test_contact_form_post_records_consent(self):
        initial_count = PrivacyConsentLog.objects.count()
        response = self.client.post('/contato/', {
            'full-name': 'Maria Oliveira',
            'email': 'maria@test.com',
            'phone': '11999998888',
            'message': 'Gostaria de conhecer o PortalK12',
            'lgpd_consent': 'on'
        })
        self.assertRedirects(response, '/contato/?success=1')
        self.assertEqual(PrivacyConsentLog.objects.count(), initial_count + 1)

    def test_legacy_aliases_redirect(self):
        self.assertRedirects(self.client.get('/servicos/'), '/solucoes/')
        self.assertRedirects(self.client.get('/projetos/'), '/recursos/')

    def test_home_two_uses_dedicated_template_and_sections(self):
        response = self.client.get('/home-two/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/home_two.html')
        content = response.content.decode('utf-8')

        # Home Two specific header/hero classes (must not reuse Home One header)
        self.assertIn('header-normal2', content)
        self.assertIn('bg-[url(\'../images/banner/2.png\')]', content)
        self.assertIn('PortalK12', content)

        # All original sections in order: Categories, About, Courses,
        # Counter, Video/Brands, WhyChoose, Achivement (pricing), BlogArticle, Footer
        for marker in [
            'Categorias',
            'Sobre O PortalK12',
            'Módulos Da Plataforma',
            'Alguns Números',
            'video-area',
            'brands-area',
            'Por Que Escolher O PortalK12',
            'active-price',
            'Confira As Últimas',
            'Nas Redes Sociais',
        ]:
            self.assertIn(marker, content)

        order = [content.find(m) for m in [
            'Categorias', 'Sobre O PortalK12', 'Módulos Da Plataforma', 'Alguns Números',
            'video-area', 'Por Que Escolher O PortalK12', 'active-price',
            'Confira As Últimas', 'Nas Redes Sociais',
        ]]
        self.assertEqual(order, sorted(order), 'Home Two sections are out of the original Edumim order')

    def test_home_two_has_no_legacy_branding(self):
        response = self.client.get('/home-two/')
        content = response.content.decode('utf-8')
        for bad in ['Intereal', 'Marmoraria', 'Santander', 'Marble', 'Interior Design', 'Get A Quote', 'Edumim']:
            self.assertNotIn(bad, content)

    def test_home_three_uses_dedicated_template_and_sections(self):
        response = self.client.get('/home-three/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/home_three.html')
        content = response.content.decode('utf-8')

        self.assertIn('bg-[url(\'../images/banner/3.png\')]', content)
        self.assertIn('filter-list', content)
        self.assertIn('accrodains', content)
        self.assertIn('swiper', content.lower())

        for marker in [
            'Home Three',
            'Cursos em destaque',
            'Junte-se a nos',
            'Cresca com o PortalK12',
            'Perguntas frequentes',
            'Confira as ultimas',
        ]:
            self.assertIn(marker, content)

    def test_home_one_has_faithful_structure(self):
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        self.assertIn('shadow-e1', content)
        self.assertIn('Começar Agora', content)
        self.assertIn('counter', content)
        self.assertIn('footer-logo.svg', content)
        self.assertIn('bxl:facebook', content)
        courses_count = content.count('shadow-box2 rounded-[8px]')
        self.assertGreaterEqual(courses_count, 12)

    def test_about_one_uses_dedicated_template_and_sections(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/about_one.html')
        content = response.content.decode('utf-8')
        self.assertIn('bred.png', content)
        self.assertIn('About Us 1', content)
        self.assertIn('progressbar-group', content)
        self.assertIn('accrodains', content)
        self.assertIn('social-explore', content)
        for marker in ['Core Features', 'Some Fun Fact', 'Testimonial', 'Team Member', 'Frequently Asked Question']:
            self.assertIn(marker, content)

    def test_about_two_uses_dedicated_template_and_sections(self):
        response = self.client.get('/about-two/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/about_two.html')
        content = response.content.decode('utf-8')
        self.assertIn('About Us 2', content)
        self.assertIn('about5.png', content)
        self.assertIn('Popular', content)
        self.assertIn('Build Your Career', content)
        self.assertIn('video-area', content)
        self.assertIn('Subscribe to My Newsletter', content)
        order = [content.find(m) for m in ['about5.png', 'Popular', 'Best Online Learning Platform', 'Build Your Career', 'video-area', 'Team Member', 'Subscribe to My Newsletter']]
        self.assertEqual(order, sorted(order))

    def test_instructor_one_uses_dedicated_template_and_sections(self):
        response = self.client.get('/instructor/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/instructor_one.html')
        content = response.content.decode('utf-8')
        self.assertIn('Instructor 1', content)
        self.assertIn('Team Member', content)
        self.assertIn('bxl:facebook', content)
        self.assertIn('Our Tallented Students Valuable', content)
        self.assertIn('swiper', content.lower())
        self.assertIn('brands-area', content)
        order = [content.find(m) for m in ['Team Member', 'Testimonial', 'brands-area']]
        self.assertEqual(order, sorted(order))

    def test_instructor_two_uses_dedicated_template_and_sections(self):
        response = self.client.get('/instructor-two/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/instructor_two.html')
        content = response.content.decode('utf-8')
        self.assertIn('Instructor 2', content)
        self.assertIn('social-explore', content)
        self.assertIn('Enrolled Students', content)
        self.assertIn('testi-left.png', content)
        self.assertIn('View All Reviews', content)
        order = [content.find(m) for m in ['social-explore', 'Enrolled Students', 'testi-left.png']]
        self.assertEqual(order, sorted(order))

    def test_instructor_details_uses_dedicated_template_and_sections(self):
        response = self.client.get('/instructor-details/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/instructor_details.html')
        content = response.content.decode('utf-8')
        self.assertIn('About Instructor', content)
        self.assertIn('Team Member 1', content)
        self.assertIn('single-ins.png', content)
        self.assertIn('insbg.png', content)
        self.assertIn('Coralina Cloud', content)
        self.assertIn('Follow Me On:', content)
        self.assertIn('Courses By Coralina', content)
        self.assertIn('View All Courses', content)

    def test_event_uses_dedicated_template_and_sections(self):
        response = self.client.get('/event/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/event.html')
        content = response.content.decode('utf-8')
        self.assertIn('Events', content)
        self.assertIn('Showing 12 courses of 52', content)
        self.assertIn('Sort By: Popularity', content)
        self.assertIn('International Art Fair 2022', content)
        self.assertIn('Book A Seat', content)
        self.assertIn('pagination', content)
        self.assertGreaterEqual(content.count('shadow-box5'), 9)

    def test_event_single_uses_dedicated_template_and_sections(self):
        response = self.client.get('/event-single/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/event_single.html')
        content = response.content.decode('utf-8')
        self.assertIn('Painting Contest 2022', content)
        self.assertIn('main-event.png', content)
        self.assertIn('id="timer"', content)
        self.assertIn('Event Details', content)
        self.assertIn('Special Guests', content)
        self.assertIn('Sofia d. Flora', content)
        self.assertIn('Jhonson Steven', content)
        order = [content.find(m) for m in ['main-event.png', 'id="timer"', 'Event Details', 'Special Guests']]
        self.assertEqual(order, sorted(order))

    def test_courses_uses_dedicated_template_and_sections(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/courses.html')
        content = response.content.decode('utf-8')
        self.assertIn('Courses', content)
        self.assertIn('Showing 12 courses of 52', content)
        self.assertIn('clarity:grid-view-line', content)
        self.assertIn('Basic Fundamentals of Interior &amp; Graphics Design', content)
        self.assertIn('Load More', content)
        self.assertGreaterEqual(content.count('shadow-box2'), 8)

    def test_courses_sidebar_uses_dedicated_template_and_sections(self):
        response = self.client.get('/courses-sidebar/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/courses_sidebar.html')
        content = response.content.decode('utf-8')
        self.assertIn('Price Filter', content)
        self.assertIn('Skill Level', content)
        self.assertIn('Rating By', content)
        self.assertIn('Search keyword', content)
        self.assertIn('lg:col-span-8', content)
        self.assertIn('lg:col-span-4', content)

    def test_single_course_uses_dedicated_template_and_sections(self):
        response = self.client.get('/single-course/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/single_course.html')
        content = response.content.decode('utf-8')
        self.assertIn('Course Details', content)
        self.assertIn('single-course-thumb.png', content)
        self.assertIn('UI/UX Design and Graphics Learning Bootcamp 2022', content)
        self.assertIn('OverView', content)
        self.assertIn('Carriculum', content)
        self.assertIn('Enroll Now', content)
        self.assertIn('Related Courses', content)
        self.assertIn('course-accrodain', content)
        order = [content.find(m) for m in ['single-course-thumb.png', 'OverView', 'Enroll Now', 'Related Courses']]
        self.assertEqual(order, sorted(order))

    def test_blog_standard_uses_dedicated_template_and_sections(self):
        response = self.client.get('/blog-standard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/blog.html')
        content = response.content.decode('utf-8')
        self.assertIn('Blog Standard', content)
        self.assertIn('shadow-box12', content)
        self.assertIn('Analytics To Help You Understand Your Customers Properly', content)
        self.assertIn('3 Min Read', content)
        self.assertIn('Popular Tags', content)
        self.assertIn('Instagram Feed', content)
        self.assertIn('pagination', content)
        self.assertGreaterEqual(content.count('h-[420px]'), 3)

    def test_single_blog_uses_dedicated_template_and_sections(self):
        response = self.client.get('/single-blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public_site/edumim/blog_detail.html')
        content = response.content.decode('utf-8')
        self.assertIn('Blog Details', content)
        self.assertIn('b-s-1.png', content)
        self.assertIn('Learn At Your Own Pace', content)
        self.assertIn('Rosalina D. Jackson', content)
        self.assertIn('3 Comments', content)
        self.assertIn('Leave A Reply', content)
        self.assertIn('Send Message', content)
        order = [content.find(m) for m in ['b-s-1.png', 'Learn At Your Own Pace', '3 Comments', 'Leave A Reply']]
        self.assertEqual(order, sorted(order))
