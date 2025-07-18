from django.core.management.base import BaseCommand
from SymptomsApp.views import initialize_models, load_faiss_index
import os

class Command(BaseCommand):
    help = 'Warm up RAG models and FAISS index'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting model warm-up...'))
        
        try:
            # Initialize models
            self.stdout.write('Initializing RAG models...')
            success = initialize_models()
            if success:
                self.stdout.write(self.style.SUCCESS('RAG models initialized successfully'))
            else:
                self.stdout.write(self.style.WARNING('RAG models initialization failed'))
            
            # Load FAISS index
            self.stdout.write('Loading FAISS index...')
            load_faiss_index()
            self.stdout.write(self.style.SUCCESS('FAISS index loaded successfully'))
            
            self.stdout.write(self.style.SUCCESS('Model warm-up completed!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Model warm-up failed: {str(e)}'))
